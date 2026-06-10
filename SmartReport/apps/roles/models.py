from django.db import models

from apps.accounts.models import CustomUser
from apps.regions.models import District # NEW


class Permission(models.Model):
    codename = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles_permission'
        ordering = ['codename']

    def __str__(self):
        return f"{self.codename}"



class Role(models.Model):
    codename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    #many to many with permission
    permissions = models.ManyToManyField(Permission, related_name='roles', blank=True)
    is_builtin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles_role'
        ordering = ['codename']

    def __str__(self):
        return f"{self.codename}"

class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    scope = models.CharField(max_length=50, blank=True)   #optional scope : 'team_engineering', 'region_123' etc
    region = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_roles') # NEW

    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='user_roles_assigned')

    class Meta:
        db_table = 'roles_user_role'
        unique_together = (('user', 'role', 'region'),) # CHANGED

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if getattr(self.role, 'codename', None) == 'ward_staff' and not self.region:
            raise ValidationError("ward_staff role must have a region assigned.")
        super().save(*args, **kwargs)

class AuditLog(models.Model):
    DECISION_CHOICES = (
    ('ALLOW', 'Access granted'),
    ('DENY', 'Access denied'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=250)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    reason = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles_auditlog'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'decision']),
            ]
