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

