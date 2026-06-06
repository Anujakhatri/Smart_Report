# Graph Report - .  (2026-05-26)

## Corpus Check
- Corpus is ~9,900 words - fits in a single context window. You may not need a graph.

## Summary
- 171 nodes · 367 edges · 34 communities detected
- Extraction: 40% EXTRACTED · 60% INFERRED · 0% AMBIGUOUS · INFERRED: 221 edges (avg confidence: 0.53)
- Token cost: 1,200 input · 800 output

## Community Hubs (Navigation)
- [[_COMMUNITY_RBAC Models & Services|RBAC Models & Services]]
- [[_COMMUNITY_Authentication & User Accounts API|Authentication & User Accounts API]]
- [[_COMMUNITY_Custom Perms & View Actions|Custom Perms & View Actions]]
- [[_COMMUNITY_Custom User Model|Custom User Model]]
- [[_COMMUNITY_RBAC Business Services|RBAC Business Services]]
- [[_COMMUNITY_Django App Configurations|Django App Configurations]]
- [[_COMMUNITY_Web Front-ends & Documentation|Web Front-ends & Documentation]]
- [[_COMMUNITY_Core Permission Constants|Core Permission Constants]]
- [[_COMMUNITY_RBAC View Decorators|RBAC View Decorators]]
- [[_COMMUNITY_Management CLI|Management CLI]]
- [[_COMMUNITY_DB Schema Initial Migrations|DB Schema Initial Migrations]]
- [[_COMMUNITY_ASGI Web Server Entry|ASGI Web Server Entry]]
- [[_COMMUNITY_Project Settings Configuration|Project Settings Configuration]]
- [[_COMMUNITY_Main URL Routing|Main URL Routing]]
- [[_COMMUNITY_WSGI Web Server Entry|WSGI Web Server Entry]]
- [[_COMMUNITY_User Model DB Schema Alteration|User Model DB Schema Alteration]]
- [[_COMMUNITY_Civic Reports URL Configuration|Civic Reports URL Configuration]]
- [[_COMMUNITY_SmartReport Init Module|SmartReport Init Module]]
- [[_COMMUNITY_Apps Init Module|Apps Init Module]]
- [[_COMMUNITY_Roles Init Module|Roles Init Module]]
- [[_COMMUNITY_Roles Admin Panel|Roles Admin Panel]]
- [[_COMMUNITY_Roles App Test Suite|Roles App Test Suite]]
- [[_COMMUNITY_Roles Routing Endpoints|Roles Routing Endpoints]]
- [[_COMMUNITY_Roles DB Migrations Folder Init|Roles DB Migrations Folder Init]]
- [[_COMMUNITY_Accounts Init Module|Accounts Init Module]]
- [[_COMMUNITY_Accounts Admin Panel|Accounts Admin Panel]]
- [[_COMMUNITY_Accounts App Test Suite|Accounts App Test Suite]]
- [[_COMMUNITY_Accounts DB Migrations Folder Init|Accounts DB Migrations Folder Init]]
- [[_COMMUNITY_Reports Model Layer|Reports Model Layer]]
- [[_COMMUNITY_Reports Admin Panel|Reports Admin Panel]]
- [[_COMMUNITY_Reports App Test Suite|Reports App Test Suite]]
- [[_COMMUNITY_Reports DB Migrations Folder Init|Reports DB Migrations Folder Init]]
- [[_COMMUNITY_README Core Civic Features|README Core Civic Features]]
- [[_COMMUNITY_GitHub PR Contribution Template|GitHub PR Contribution Template]]

## God Nodes (most connected - your core abstractions)
1. `Role` - 27 edges
2. `RBACService` - 26 edges
3. `Permission` - 24 edges
4. `UserRole` - 24 edges
5. `AuditLog` - 23 edges
6. `CheckPermissionView` - 16 edges
7. `RBACStatsView` - 16 edges
8. `UserRoleViewSet` - 15 edges
9. `PermissionViewSet` - 14 edges
10. `RoleViewSet` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Check if user has the required permission.` --uses--> `RBACService`  [INFERRED]
  SmartReport/apps/roles/permissions.py → SmartReport/apps/roles/services.py
- `Decorator requiring admin role.` --uses--> `RBACService`  [INFERRED]
  SmartReport/apps/roles/decorators.py → SmartReport/apps/roles/services.py
- `Secure Profile Page` --implements--> `Smart Report Tech Stack`  [INFERRED]
  SmartReport/templates/profile.html → README.md
- `User Registration Page` --implements--> `Smart Report Tech Stack`  [INFERRED]
  SmartReport/templates/register.html → README.md
- `User Authentication Sign In Page` --implements--> `Smart Report Tech Stack`  [INFERRED]
  SmartReport/templates/login.html → README.md

## Hyperedges (group relationships)
- **Smart Report User Interfaces** — home_page, profile_page, register_page, login_page [EXTRACTED 0.90]
- **JWT User Authentication Flow** — login_page, register_page, profile_page, readme_tech_stack [INFERRED 0.85]

## Communities

### Community 0 - "RBAC Models & Services"
Cohesion: 0.23
Nodes (33): BasePermission, AuditLog, Permission, Role, UserRole, CanCreateReport, HasPermission, IsAdmin (+25 more)

### Community 1 - "Authentication & User Accounts API"
Cohesion: 0.13
Nodes (19): APIView, get_token(), LoginSerializer, LogoutSerializer, Validates fields and creates the user.     Token minting is the view's job — not, validate() → confirms token string is present     save()     → blacklists it so, roles → SerializerMethodField because it's get_roles() not a db column.      Use, RegisterSerializer (+11 more)

### Community 2 - "Custom Perms & View Actions"
Cohesion: 0.15
Nodes (8): Check if user has the required permission., add_permission(), by_role(), by_user(), home(), remove_permission(), user_activity(), users()

### Community 3 - "Custom User Model"
Cohesion: 0.2
Nodes (7): AbstractUser, CustomUser, Meta, Get all roles for this user., get all distinct permissions for this user., Extended Django user model with RBAC support., get_user_permissions()

### Community 4 - "RBAC Business Services"
Cohesion: 0.33
Nodes (5): assign_role(), can_edit_report(), can_view_report(), has_permission(), _log_access()

### Community 5 - "Django App Configurations"
Cohesion: 0.29
Nodes (4): AppConfig, AccountsConfig, ReportsConfig, RolesConfig

### Community 6 - "Web Front-ends & Documentation"
Cohesion: 0.38
Nodes (7): Home & Landing Page, User Authentication Sign In Page, Secure Profile Page, Smart Report NP, Smart Report Tech Stack, User Registration Page, Project Dependencies

### Community 7 - "Core Permission Constants"
Cohesion: 0.33
Nodes (5): DashboardPermissions, Single source of truth for ALL permission codenames. Import from here everywhere, RegionPermissions, ReportPermissions, UserPermissions

### Community 8 - "RBAC View Decorators"
Cohesion: 0.4
Nodes (4): Decorator requiring admin role., Decorator for function-based views.      Usage:         @api_view(['POST']), require_admin(), require_permission()

### Community 9 - "Management CLI"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 10 - "DB Schema Initial Migrations"
Cohesion: 0.67
Nodes (1): Migration

### Community 11 - "ASGI Web Server Entry"
Cohesion: 1.0
Nodes (1): ASGI config for SmartReport project.  It exposes the ASGI callable as a module-l

### Community 12 - "Project Settings Configuration"
Cohesion: 1.0
Nodes (1): Django settings for SmartReport project.  Generated by 'django-admin startprojec

### Community 13 - "Main URL Routing"
Cohesion: 1.0
Nodes (1): URL configuration for SmartReport project.  The `urlpatterns` list routes URLs t

### Community 14 - "WSGI Web Server Entry"
Cohesion: 1.0
Nodes (1): WSGI config for SmartReport project.  It exposes the WSGI callable as a module-l

### Community 15 - "User Model DB Schema Alteration"
Cohesion: 1.0
Nodes (1): Migration

### Community 16 - "Civic Reports URL Configuration"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "SmartReport Init Module"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Apps Init Module"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Roles Init Module"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Roles Admin Panel"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Roles App Test Suite"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Roles Routing Endpoints"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Roles DB Migrations Folder Init"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Accounts Init Module"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Accounts Admin Panel"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Accounts App Test Suite"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Accounts DB Migrations Folder Init"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Reports Model Layer"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Reports Admin Panel"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Reports App Test Suite"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Reports DB Migrations Folder Init"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "README Core Civic Features"
Cohesion: 1.0
Nodes (1): Civic Reporting Features

### Community 33 - "GitHub PR Contribution Template"
Cohesion: 1.0
Nodes (1): GitHub Pull Request Template

## Knowledge Gaps
- **19 isolated node(s):** `Run administrative tasks.`, `ASGI config for SmartReport project.  It exposes the ASGI callable as a module-l`, `Django settings for SmartReport project.  Generated by 'django-admin startprojec`, `URL configuration for SmartReport project.  The `urlpatterns` list routes URLs t`, `WSGI config for SmartReport project.  It exposes the WSGI callable as a module-l` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `ASGI Web Server Entry`** (2 nodes): `ASGI config for SmartReport project.  It exposes the ASGI callable as a module-l`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project Settings Configuration`** (2 nodes): `Django settings for SmartReport project.  Generated by 'django-admin startprojec`, `settings.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Main URL Routing`** (2 nodes): `urls.py`, `URL configuration for SmartReport project.  The `urlpatterns` list routes URLs t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `WSGI Web Server Entry`** (2 nodes): `wsgi.py`, `WSGI config for SmartReport project.  It exposes the WSGI callable as a module-l`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `User Model DB Schema Alteration`** (2 nodes): `Migration`, `0002_alter_customuser_created_at_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Civic Reports URL Configuration`** (2 nodes): `__init__.py`, `urls.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `SmartReport Init Module`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Apps Init Module`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Roles Init Module`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Roles Admin Panel`** (1 nodes): `admin.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Roles App Test Suite`** (1 nodes): `tests.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Roles Routing Endpoints`** (1 nodes): `urls.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Roles DB Migrations Folder Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accounts Init Module`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accounts Admin Panel`** (1 nodes): `admin.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accounts App Test Suite`** (1 nodes): `tests.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accounts DB Migrations Folder Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Reports Model Layer`** (1 nodes): `models.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Reports Admin Panel`** (1 nodes): `admin.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Reports App Test Suite`** (1 nodes): `tests.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Reports DB Migrations Folder Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `README Core Civic Features`** (1 nodes): `Civic Reporting Features`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GitHub PR Contribution Template`** (1 nodes): `GitHub Pull Request Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RBACService` connect `RBAC Models & Services` to `RBAC View Decorators`, `Custom Perms & View Actions`, `Custom User Model`, `RBAC Business Services`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `Meta` connect `RBAC Models & Services` to `Authentication & User Accounts API`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `RBACStatsView` connect `RBAC Models & Services` to `Authentication & User Accounts API`, `Custom Perms & View Actions`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `Role` (e.g. with `RBACService` and `Centralized service for all RBAC operations.`) actually correct?**
  _`Role` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `RBACService` (e.g. with `Permission` and `Role`) actually correct?**
  _`RBACService` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Permission` (e.g. with `RBACService` and `Centralized service for all RBAC operations.`) actually correct?**
  _`Permission` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `UserRole` (e.g. with `RBACService` and `Centralized service for all RBAC operations.`) actually correct?**
  _`UserRole` has 22 INFERRED edges - model-reasoned connections that need verification._