from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/rbac/',include('apps.roles.urls')),
    path('api/reports/',include('apps.reports.urls')),
    path('api/regions/',include('apps.regions.urls')),
]


