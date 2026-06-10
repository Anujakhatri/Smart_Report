from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    """Extended Django user model with RBAC support."""

    PROVINCE_CHOICES = (
        ('koshi',         'Koshi Province'),
        ('madhesh',       'Madhesh Province'),
        ('bagmati',       'Bagmati Province'),
        ('gandaki',       'Gandaki Province'),
        ('lumbini',       'Lumbini Province'),
        ('karnali',       'Karnali Province'),
        ('sudurpashchim', 'Sudurpashchim Province'),
    )

    #actual db column
    phone_number = models.CharField( max_length=20, blank=True, null=True)
    province = models.CharField( max_length=50, choices=PROVINCE_CHOICES, blank=True, null=True, help_text="Only applicable for citizen and province staff.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def get_roles(self):
        """Get all roles for this user."""
        from apps.roles.models import Role
        return Role.objects.filter(
            user_roles__user=self
        ).distinct()

   
    def get_permissions(self):
        """get all distinct permissions for this user."""
        from apps.roles.services import RBACService
        return RBACService.get_user_permissions(self)    