import logging
from apps.roles.models import Permission, Role, UserRole, AuditLog

logger = logging.getLogger(__name__)


class RBACService:
    """Centralized service for all RBAC operations."""

    @staticmethod
    def has_permission(user, permission_codename, resource=None):
        """
        Check if user has a specific permission.

        Args:
            user: User object
            permission_codename: 'report.create', 'user.admin', etc.
            resource: Optional resource identifier for logging

        Returns:
            (bool, str) - (has_permission, reason)
        """
        if not user or not user.is_authenticated:
            return False, "User not authenticated"

        if user.is_superuser:
            return True, "Superuser bypass"

        # Get all roles for this user
        user_roles = UserRole.objects.filter(
            user=user
        ).select_related('role')

        if not user_roles.exists():
            return False, "User has no roles"

        # Check if any role has this permission
        has_perm = Permission.objects.filter(
            codename=permission_codename,
            roles__in=[ur.role for ur in user_roles]
        ).exists()

        reason = "Permission granted via role" if has_perm else "Permission denied"

        # Log the decision
        RBACService._log_access(user, permission_codename, resource,
                                has_perm, reason)

        return has_perm, reason

    @staticmethod
    def get_user_roles(user):
        """Get all roles for a user."""
        return Role.objects.filter(
            userrole__user=user
        ).distinct()

    @staticmethod
    def get_user_permissions(user):
        """Get all permissions for a user (flattened)."""
        return Permission.objects.filter(
            roles__userrole__user=user
        ).distinct()

    @staticmethod
    def assign_role(user, role, assigned_by=None, scope=''):
        """
        Assign a role to a user.

        Args:
            user: User object
            role: Role object or codename (str)
            assigned_by: User who assigned (optional)
            scope: Scope string (e.g., 'region_123')
        """
        if isinstance(role, str):
            role = Role.objects.get(codename=role)

        user_role, created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            scope=scope,
            defaults={'assigned_by': assigned_by}
        )

        if created:
            logger.info(
                f"Assigned role {role.codename} to user {user.username}"
            )

        return user_role

    @staticmethod
    def can_view_report(user, report):
        """Check if user can view a specific report."""
        if user.is_superuser:
            return True

        has_perm, _ = RBACService.has_permission(user, 'report.view')
        if not has_perm:
            return False

        # Rule: User owns it OR is in same region
        if report.created_by == user:
            return True

        # Check regional scope
        if report.region:
            return UserRole.objects.filter(
                user=user,
                scope__startswith=f'region_{report.region.id}'
            ).exists()

        return True

    @staticmethod
    def can_edit_report(user, report):
        """Check if user can edit a specific report."""
        if user.is_superuser:
            return True

        has_perm, _ = RBACService.has_permission(user, 'report.edit')
        if not has_perm:
            return False

        # Only owner or regional admin can edit
        return (report.created_by == user or
                UserRole.objects.filter(
                    user=user,
                    role__codename='regional_admin'
                ).exists())

    @staticmethod
    def _log_access(user, action, resource, allowed, reason,
                    ip_address=None, user_agent=None):
        """Log an access decision to AuditLog."""
        AuditLog.objects.create(
            user=user,
            action=action,
            resource=resource or '',
            decision='ALLOW' if allowed else 'DENY',
            reason=reason,
            ip_address=ip_address,
            user_agent=user_agent,
        )