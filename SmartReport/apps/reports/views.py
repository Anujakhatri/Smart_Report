from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError

from core.constants import ReportPermissions
from apps.roles.decorators import require_permission
from apps.roles.services import RBACService
from apps.roles.models import AuditLog, UserRole
from apps.reports.models import Report, ReportImage, ReportCluster, STATUS_TRANSITIONS
from apps.reports.serializers import (
    ReportListSerializer,
    ReportDetailSerializer,
    ReportCreateSerializer,
    ReportUpdateSerializer,
    ReportImageSerializer,
    ReportClusterSerializer,
    MapMarkerSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from apps.reports.filters import ReportFilter

try:
    from core.pagination import CustomPagination
except ImportError:
    from rest_framework.pagination import PageNumberPagination
    class CustomPagination(PageNumberPagination):
        page_size = 10

User = get_user_model()


class BaseResponseMixin:
    """Mixin to format standard responses consistently."""
    def get_success_response(self, data, message="Success", status_code=status.HTTP_200_OK):
        return Response({
            "success": True,
            "data": data,
            "message": message
        }, status=status_code)

    def get_error_response(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "success": False,
            "data": None,
            "message": message
        }, status=status_code)


class ReportViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = Report.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReportFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ReportListSerializer
        elif self.action == 'retrieve':
            return ReportDetailSerializer
        elif self.action in ['create']:
            return ReportCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReportUpdateSerializer
        return ReportDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Report.objects.none()

        # Check if user has permission to view all reports across Nepal
        has_view_all, _ = RBACService.has_permission(user, ReportPermissions.VIEW_ALL)
        if has_view_all:
            return Report.objects.all()

        # Check if user has permission to view province reports
        has_view_province, _ = RBACService.has_permission(user, ReportPermissions.VIEW_PROVINCE)
        if has_view_province:
            user_scopes = UserRole.objects.filter(user=user).values_list('scope', flat=True)
            district_ids = []
            for scope in user_scopes:
                if scope.startswith('region_'):
                    district_ids.append(scope.replace('region_', ''))
            return Report.objects.filter(region_id__in=district_ids)

        # Citizens / standard users can only view their own
        return Report.objects.filter(submitted_by=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return self.get_success_response(paginated_response.data, "List retrieved successfully")
        
        serializer = self.get_serializer(queryset, many=True)
        return self.get_success_response(serializer.data, "List retrieved successfully")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Enforce RBAC dynamic check
        if not RBACService.can_view_report(request.user, instance):
            return self.get_error_response("Access Denied to this report details.", status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return self.get_success_response(serializer.data, "Details retrieved successfully")

    @method_decorator(require_permission(ReportPermissions.SUBMIT))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Validate image limits and size from raw request files before creating
        images = request.FILES.getlist('images')
        if len(images) > 5:
            raise ValidationError("You can upload a maximum of 5 images.")
        
        for img in images:
            if img.size > 10 * 1024 * 1024:
                raise ValidationError("Each image must be less than 10MB.")

        # Save report
        report = serializer.save(submitted_by=request.user)

        # Save images
        for img in images:
            ReportImage.objects.create(report=report, image=img)

        # Audit log creation
        AuditLog.objects.create(
            user=request.user,
            action='create',
            resource=f"report_{report.id}",
            decision='ALLOW',
            reason='User submitted a new report with images',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        detail_serializer = ReportDetailSerializer(report)
        return self.get_success_response(detail_serializer.data, "Report created successfully", status.HTTP_201_CREATED)

    @method_decorator(require_permission(ReportPermissions.REVIEW))
    def update(self, request, *args, **kwargs):
        return self._perform_update(request, *args, **kwargs)

    @method_decorator(require_permission(ReportPermissions.REVIEW))
    def partial_update(self, request, *args, **kwargs):
        return self._perform_update(request, *args, **kwargs)

    def _perform_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        old_status = instance.status
        new_status = serializer.validated_data.get('status', old_status)
        old_priority = instance.priority
        new_priority = serializer.validated_data.get('priority', old_priority)
        old_assigned = instance.assigned_to
        new_assigned = serializer.validated_data.get('assigned_to', old_assigned)

        # 1. Check priority edit permission
        if old_priority != new_priority:
            has_priority_perm, _ = RBACService.has_permission(request.user, ReportPermissions.CHANGE_PRIORITY)
            if not has_priority_perm:
                return self.get_error_response("Permission denied to change priority.", status.HTTP_403_FORBIDDEN)

        # 2. Check status transition validity
        if old_status != new_status:
            allowed = STATUS_TRANSITIONS.get(old_status, [])
            if new_status not in allowed:
                return self.get_error_response(f"Transition from '{old_status}' to '{new_status}' is not allowed.")

        # Save update
        report = serializer.save()

        # Audit log for status change
        if old_status != new_status:
            AuditLog.objects.create(
                user=request.user,
                action='status_change',
                resource=f"report_{report.id}",
                decision='ALLOW',
                reason=f"Status changed from {old_status} to {new_status}",
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

        # Audit log for assignment
        if old_assigned != new_assigned:
            AuditLog.objects.create(
                user=request.user,
                action='assign',
                resource=f"report_{report.id}",
                decision='ALLOW',
                reason=f"Report assigned to {new_assigned.username if new_assigned else 'None'}",
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

        detail_serializer = ReportDetailSerializer(report)
        return self.get_success_response(detail_serializer.data, "Report updated successfully")

    @method_decorator(require_permission(ReportPermissions.DELETE))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        report_id = instance.id
        instance.delete()

        # Audit log deletion
        AuditLog.objects.create(
            user=request.user,
            action='delete',
            resource=f"report_{report_id}",
            decision='ALLOW',
            reason='Report deleted by admin',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return self.get_success_response(None, "Report deleted successfully", status.HTTP_204_NO_CONTENT)

    # Custom transition endpoints
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        report = self.get_object()
        if report.submitted_by != request.user:
            return self.get_error_response("You are not the owner of this draft.", status.HTTP_403_FORBIDDEN)

        old_status = report.status
        new_status = 'submitted'
        
        allowed = STATUS_TRANSITIONS.get(old_status, [])
        if new_status not in allowed:
            return self.get_error_response(f"Transition from '{old_status}' to '{new_status}' is not allowed.")

        report.status = new_status
        report.submitted_at = timezone.now()
        report.save()

        AuditLog.objects.create(
            user=request.user,
            action='status_change',
            resource=f"report_{report.id}",
            decision='ALLOW',
            reason=f"Draft submitted by owner.",
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return self.get_success_response(ReportDetailSerializer(report).data, "Report submitted successfully")

    @action(detail=True, methods=['post'])
    @method_decorator(require_permission(ReportPermissions.REVIEW))
    def approve(self, request, pk=None):
        report = self.get_object()
        old_status = report.status
        new_status = 'approved'

        allowed = STATUS_TRANSITIONS.get(old_status, [])
        if new_status not in allowed:
            return self.get_error_response(f"Transition from '{old_status}' to '{new_status}' is not allowed.")

        report.status = new_status
        report.save()

        AuditLog.objects.create(
            user=request.user,
            action='approve',
            resource=f"report_{report.id}",
            decision='ALLOW',
            reason=f"Report approved.",
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return self.get_success_response(ReportDetailSerializer(report).data, "Report approved successfully")

    @action(detail=True, methods=['post'])
    @method_decorator(require_permission(ReportPermissions.REVIEW))
    def reject(self, request, pk=None):
        report = self.get_object()
        reason = request.data.get('rejection_reason')
        if not reason:
            return self.get_error_response("rejection_reason field is required.")

        old_status = report.status
        new_status = 'rejected'

        allowed = STATUS_TRANSITIONS.get(old_status, [])
        if new_status not in allowed:
            return self.get_error_response(f"Transition from '{old_status}' to '{new_status}' is not allowed.")

        report.status = new_status
        report.rejection_reason = reason
        report.save()

        AuditLog.objects.create(
            user=request.user,
            action='reject',
            resource=f"report_{report.id}",
            decision='ALLOW',
            reason=f"Report rejected. Reason: {reason}",
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return self.get_success_response(ReportDetailSerializer(report).data, "Report rejected successfully")

    @action(detail=True, methods=['post'])
    @method_decorator(require_permission(ReportPermissions.REVIEW))
    def assign(self, request, pk=None):
        report = self.get_object()
        user_id = request.data.get('assigned_to')
        if not user_id:
            return self.get_error_response("assigned_to (user_id) field is required.")
        
        try:
            assignee = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return self.get_error_response("Target assignee user not found.", status.HTTP_404_NOT_FOUND)

        report.assigned_to = assignee
        report.save()

        AuditLog.objects.create(
            user=request.user,
            action='assign',
            resource=f"report_{report.id}",
            decision='ALLOW',
            reason=f"Report assigned to {assignee.username}.",
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return self.get_success_response(ReportDetailSerializer(report).data, "Report assigned successfully")

    @action(detail=True, methods=['post'])
    @method_decorator(require_permission(ReportPermissions.CLOSE))
    def resolve(self, request, pk=None):
        report = self.get_object()
        old_status = report.status
        new_status = 'resolved'

        allowed = STATUS_TRANSITIONS.get(old_status, [])
        if new_status not in allowed:
            return self.get_error_response(f"Transition from '{old_status}' to '{new_status}' is not allowed.")

        report.status = new_status
        report.save()

        AuditLog.objects.create(
            user=request.user,
            action='resolve',
            resource=f"report_{report.id}",
            decision='ALLOW',
            reason=f"Report resolved.",
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return self.get_success_response(ReportDetailSerializer(report).data, "Report resolved successfully")


class ReportClusterViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = ReportCluster.objects.all()
    serializer_class = ReportClusterSerializer
    permission_classes = [IsAuthenticated]

    # TODO: Add dynamic permission mappings for merge actions
    def get_permissions(self):
        # We can implement general ViewSet rules or method decoration
        return super().get_permissions()

    @method_decorator(require_permission(ReportPermissions.MERGE_CLUSTER))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cluster = serializer.save(created_by=request.user)
        return self.get_success_response(serializer.data, "Cluster created successfully", status.HTTP_201_CREATED)

    @method_decorator(require_permission(ReportPermissions.MERGE_CLUSTER))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(require_permission(ReportPermissions.MERGE_CLUSTER))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    @method_decorator(require_permission(ReportPermissions.MERGE_CLUSTER))
    def add_report(self, request, pk=None):
        cluster = self.get_object()
        report_id = request.data.get('report_id')
        if not report_id:
            return self.get_error_response("report_id field is required.")

        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return self.get_error_response("Report not found.", status.HTTP_404_NOT_FOUND)

        cluster.reports.add(report)
        return self.get_success_response(ReportClusterSerializer(cluster).data, "Report added to cluster successfully")

    @action(detail=True, methods=['post'])
    @method_decorator(require_permission(ReportPermissions.MERGE_CLUSTER))
    def remove_report(self, request, pk=None):
        cluster = self.get_object()
        report_id = request.data.get('report_id')
        if not report_id:
            return self.get_error_response("report_id field is required.")

        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return self.get_error_response("Report not found.", status.HTTP_404_NOT_FOUND)

        cluster.reports.remove(report)
        return self.get_success_response(ReportClusterSerializer(cluster).data, "Report removed from cluster successfully")


class MapMarkerView(BaseResponseMixin, generics.ListAPIView):
    """
    Public endpoint to retrieve simple markers for public map.
    NO AUTHENTICATION REQUIRED.
    """
    permission_classes = [AllowAny]
    serializer_class = MapMarkerSerializer
    queryset = Report.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReportFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        # Support ?updated_after=<ISO timestamp> query param
        updated_after = self.request.query_params.get('updated_after')
        if updated_after:
            try:
                queryset = queryset.filter(updated_at__gt=updated_after)
            except ValidationError:
                # Handle potential invalid datetime strings gracefully
                pass
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return self.get_success_response(serializer.data, "Map markers retrieved successfully")
