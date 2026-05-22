from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.roles.services import RBACService

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