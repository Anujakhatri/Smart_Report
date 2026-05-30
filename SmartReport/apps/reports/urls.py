from django.urls import path
from .views import ReportCreateView, MyReportView

urlpatterns = [
    path('', ReportCreateView.as_view(), name='report-create'),
    path('my/', MyReportView.as_view(), name='my-reports'),
]







