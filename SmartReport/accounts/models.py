from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    #actual db column
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='citizen',
    )

    #read only computed property which doesn't touch database
    @property
    def effective_role(self):
        if self.is_superuser:
            return 'admin'
        return self.role

    #check ps is already hashed, if not hash first via set_password() then call super().save(*args, **kwargs) to prevent double-hashing
    def save(self, *args, **kwargs):
        from django.contrib.auth.hashers import is_password_usable
        if self.password and not is_password_usable(self.password):
            self.set_password(self.password)
        super().save(*args, **kwargs)
    #save function is like receptionist- it does the password check first,
    #then hands everything off to Django's original save() untouched.or
    ## a receptionist that accepts any message and forwards it exactly

    def __str__(self):
        return f"{self.username} ({self.effective_role})"

    