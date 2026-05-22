from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.roles import views

# Create routers for ViewSet endpoints
router = DefaultRouter()
router.register(r'permissions', views.PermissionViewSet, basename='permission')
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'user-roles', views.UserRoleViewSet, basename='user-role')
router.register(r'audit-logs', views.AuditLogViewSet, basename='audit-log')

app_name = 'roles'

urlpatterns = [
    # Router-based ViewSet endpoints
    path('', include(router.urls)),

    # Custom endpoints
    path('check-permission/', views.CheckPermissionView.as_view(), name='check-permission'),
    path('stats/', views.RBACStatsView.as_view(), name='rbac-stats'),
]