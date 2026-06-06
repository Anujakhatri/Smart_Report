from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.regions.views import ProvinceViewSet, DistrictViewSet

router = DefaultRouter()
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'districts', DistrictViewSet, basename='district')

urlpatterns = [
    path('', include(router.urls)),
]
