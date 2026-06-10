import os
import django

# Setup Django if run as script
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartReport.settings')
    django.setup()

from apps.roles.models import Role, Permission
from apps.core.constants import ALL_PERMISSIONS, ROLE_PERMISSION_MAP

def seed_roles_and_permissions():
    print("Seeding permissions...")
    # First, create all defined permissions
    for codename, resource, description in ALL_PERMISSIONS:
        name = description
        if len(name) > 200:
            name = name[:197] + "..."
        Permission.objects.get_or_create(
            codename=codename,
            defaults={
                'name': name,
                'description': description
            }
        )
        
    print("Seeding roles...")
    for role_code, perms in ROLE_PERMISSION_MAP.items():
        role, created = Role.objects.get_or_create(
            codename=role_code,
            defaults={
                'name': role_code.replace('_', ' ').title(),
                'is_builtin': True
            }
        )
        
        # assign permissions
        if '__all__' in perms:
            # National Admin gets all
            role.permissions.set(Permission.objects.all())
        else:
            perm_objs = Permission.objects.filter(codename__in=perms)
            role.permissions.set(perm_objs)
            
        print(f"Role '{role_code}' seeded with {role.permissions.count()} permissions.")

if __name__ == '__main__':
    seed_roles_and_permissions()
