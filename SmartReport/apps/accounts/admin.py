from django.contrib import admin
from apps.roles.models import Role, Permission, UserRole, AuditLog

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('codename', 'name', 'is_builtin')
    filter_horizontal = ('permissions',)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('codename', 'name')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'region', 'assigned_at')
    list_filter = ('role',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'decision', 'timestamp')
    readonly_fields = ('user', 'action', 'resource', 'decision', 'reason', 'timestamp')