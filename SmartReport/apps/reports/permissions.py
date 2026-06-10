from rest_framework.permissions import BasePermission
from apps.roles.models import UserRole

class IsCitizen(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return UserRole.objects.filter(user=request.user, role__codename='citizen').exists()

    def has_object_permission(self, request, view, obj):
        return obj.submitted_by == request.user


class IsWardStaff(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return UserRole.objects.filter(user=request.user, role__codename='ward_staff').exists()

    def has_object_permission(self, request, view, obj):
        # Update status allowed only if assigned
        if view.action in ['update', 'partial_update', 'resolve']:
            return getattr(obj, 'assigned_to_id', None) == request.user.id
            
        allowed_regions = UserRole.objects.filter(user=request.user, role__codename='ward_staff').values_list('region', flat=True)
        return getattr(obj, 'region_id', None) in allowed_regions or getattr(obj, 'assigned_to_id', None) == request.user.id


class IsDistrictAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return UserRole.objects.filter(user=request.user, role__codename='district_admin').exists()

    def has_object_permission(self, request, view, obj):
        allowed_regions = UserRole.objects.filter(user=request.user, role__codename='district_admin').values_list('region', flat=True)
        return getattr(obj, 'region_id', None) in allowed_regions


class IsNationalAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or UserRole.objects.filter(user=request.user, role__codename='national_admin').exists()

    def has_object_permission(self, request, view, obj):
        return True
