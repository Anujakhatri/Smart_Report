from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reports.views import ReportViewSet, ReportClusterViewSet, MapMarkerView

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'report-clusters', ReportClusterViewSet, basename='report-cluster')

# TODO: In the future, we could introduce swagger/redoc documentation routes here
urlpatterns = [
    path('reports/map-markers/', MapMarkerView.as_view(), name='map-markers'),
    path('', include(router.urls)),
]
