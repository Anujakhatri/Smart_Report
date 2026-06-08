from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.roles.services import RBACService
from apps.roles.models import UserRole # NEW

class HasPermission(BasePermission):
    """Generic permission class for any permission codename.
    usage on a view:
    require_permission = 'report.view'
    """

    message = "You don't have permission for this action."

    def has_permission(self, request, view):
        """Check if user has the required permission."""

        if not request.user or not request.user.is_authenticated:
            return False

        # View specifies required_permission
        required_perm = getattr(view, 'required_permission', None)
        #fail closed : if view forgets to set required_permission, deny access
        if not required_perm:
            return True

        has_perm, _ = RBACService.has_permission(request.user, required_perm)
        return has_perm


class IsAdmin(BasePermission):
    """User has admin role."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        has_perm, _ = RBACService.has_permission(request.user, 'user.admin')
        return has_perm


class IsReportOwnerOrReadOnly(BasePermission):
    """Owner can edit; others can only view."""

    def has_object_permission(self, request, view, obj):
        # Read permissions
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return RBACService.can_view_report(request.user, obj)

        # Write permissions
        return RBACService.can_edit_report(request.user, obj)


class CanCreateReport(BasePermission):
    """User has permission to create reports."""

    message = "You don't have permission to create reports."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method != 'POST':
            return True

        has_perm, _ = RBACService.has_permission(request.user, 'report.create')
        return has_perm


class IsCitizen(BasePermission): # NEW
    def has_permission(self, request, view): # NEW
        if not request.user or not request.user.is_authenticated: # NEW
            return False # NEW
        return UserRole.objects.filter(user=request.user, role__codename='citizen').exists() # NEW

    def has_object_permission(self, request, view, obj): # NEW
        return obj.submitted_by == request.user # NEW


class IsFieldOfficer(BasePermission): # NEW
    def has_permission(self, request, view): # NEW
        if not request.user or not request.user.is_authenticated: # NEW
            return False # NEW
        return UserRole.objects.filter(user=request.user, role__codename='field_officer').exists() # NEW

    def has_object_permission(self, request, view, obj): # NEW
        allowed_regions = UserRole.objects.filter(user=request.user, role__codename='field_officer').values_list('region', flat=True) # NEW
        return getattr(obj, 'region_id', None) in allowed_regions # NEW


class IsRegionAdmin(BasePermission): # NEW
    def has_permission(self, request, view): # NEW
        if not request.user or not request.user.is_authenticated: # NEW
            return False # NEW
        return UserRole.objects.filter(user=request.user, role__codename='region_admin').exists() # NEW

    def has_object_permission(self, request, view, obj): # NEW
        allowed_regions = UserRole.objects.filter(user=request.user, role__codename='region_admin').values_list('region', flat=True) # NEW
        return getattr(obj, 'region_id', None) in allowed_regions # NEW


class IsSuperAdmin(BasePermission): # NEW
    def has_permission(self, request, view): # NEW
        if not request.user or not request.user.is_authenticated: # NEW
            return False # NEW
        return request.user.is_superuser or UserRole.objects.filter(user=request.user, role__codename='super_admin').exists() # NEW

    def has_object_permission(self, request, view, obj): # NEW
        return True # NEW