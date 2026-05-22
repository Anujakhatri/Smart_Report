from rest_framework import serializers
from .models import Permission, Role, UserRole, AuditLog


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'codename', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    # ── WRITE — accept permission IDs on POST/PUT ─────────────────
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        write_only=True,
        source='permissions',
    )

    class Meta:
        model = Role
        fields = ('id', 'codename', 'name', 'description', 'is_builtin',
                  'permissions', 'permission_ids',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserRoleSerializer(serializers.ModelSerializer):
    #READ - nested objects on GET
    role = RoleSerializer(read_only=True)
    assigned_by = serializers.StringRelatedField(read_only=True)

    # ── WRITE — accept role ID on POST ────────────────────────────
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        write_only=True,
        source='role',
    )
    class Meta:
        model = UserRole
        fields = ('id', 'user', 'role', 'role_id', 'scope', 'assigned_at', 'assigned_by')
        read_only_fields = ('id', 'assigned_at', 'assigned_by')


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

    def get_fields(self):
        fields = super(AuditLogSerializer, self).get_fields()
        for field in fields.values():
            field.read_only=True
        return fields
