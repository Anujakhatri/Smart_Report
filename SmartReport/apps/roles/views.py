from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.roles.models import Permission, Role, UserRole, AuditLog
from apps.roles.serializers import (
    PermissionSerializer,
    RoleSerializer,
    UserRoleSerializer,
    AuditLogSerializer,
)
from apps.roles.services import RBACService
from apps.roles.permissions import HasPermission, IsAdmin

User = get_user_model()


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-role')
    def by_role(self, request):
        role_id = request.query_params.get('role_id')
        if not role_id:
            return Response({'detail': 'role_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role = Role.objects.get(id=role_id)
            permissions = role.permissions.all()
            serializer = self.get_serializer(permissions, many=True)
            return Response(serializer.data)
        except Role.DoesNotExist:
            return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        role = self.get_object()
        user_roles = UserRole.objects.filter(role=role)
        users = [ur.user for ur in user_roles]
        data = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
        return Response(data)

    @action(detail=True, methods=['post'], url_path='add-permission')
    def add_permission(self, request, pk=None):
        role = self.get_object()
        permission_id = request.data.get('permission_id')
        if not permission_id:
            return Response({'detail': 'permission_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            permission = Permission.objects.get(id=permission_id)
            role.permissions.add(permission)
            return Response({'detail': f'Permission {permission.codename} added to role {role.codename}.'})
        except Permission.DoesNotExist:
            return Response({'detail': 'Permission not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='remove-permission')
    def remove_permission(self, request, pk=None):
        role = self.get_object()
        permission_id = request.data.get('permission_id')
        if not permission_id:
            return Response({'detail': 'permission_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            permission = Permission.objects.get(id=permission_id)
            role.permissions.remove(permission)
            return Response({'detail': f'Permission {permission.codename} removed from role {role.codename}.'})
        except Permission.DoesNotExist:
            return Response({'detail': 'Permission not found.'}, status=status.HTTP_404_NOT_FOUND)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='by-user')
    def by_user(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user_roles = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(user_roles, many=True)
        return Response(serializer.data)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='user-activity')
    def user_activity(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        logs = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='recent-denials')
    def recent_denials(self, request):
        logs = self.queryset.filter(decision='DENY')[:50]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        total_logs = self.queryset.count()
        total_allows = self.queryset.filter(decision='ALLOW').count()
        total_denies = self.queryset.filter(decision='DENY').count()
        return Response({
            'total_logs': total_logs,
            'allows': total_allows,
            'denies': total_denies,
        })


class CheckPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        permission_codename = request.data.get('permission')
        resource = request.data.get('resource')
        if not permission_codename:
            return Response({'detail': 'permission codename is required.'}, status=status.HTTP_400_BAD_REQUEST)

        has_perm, reason = RBACService.has_permission(request.user, permission_codename, resource)
        return Response({
            'has_permission': has_perm,
            'reason': reason
        })


class RBACStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_users = User.objects.count()
        total_roles = Role.objects.count()
        total_permissions = Permission.objects.count()
        total_assignments = UserRole.objects.count()
        return Response({
            'total_users': total_users,
            'total_roles': total_roles,
            'total_permissions': total_permissions,
            'total_assignments': total_assignments,
        })



