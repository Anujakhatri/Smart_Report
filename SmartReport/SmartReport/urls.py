from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import CitizenLoginView, WardLoginView, DistrictLoginView, AdminLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/rbac/',include('apps.roles.urls')),
    path('api/reports/',include('apps.reports.urls')),
    path('api/regions/',include('apps.regions.urls')),
    
    # Portal specific login endpoints
    path('citizen/auth/login/', CitizenLoginView.as_view(), name='citizen_login'),
    path('ward/auth/login/', WardLoginView.as_view(), name='ward_login'),
    path('district/auth/login/', DistrictLoginView.as_view(), name='district_login'),
    path('admin-portal/auth/login/', AdminLoginView.as_view(), name='admin_login'),
]
