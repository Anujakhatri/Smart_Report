from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.reports.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register_page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login_page'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile_page'),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/rbac/', include('apps.roles.urls')),
    path('api/reports/', include('apps.reports.urls')),
]
