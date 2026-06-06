import django_filters
from apps.reports.models import Report

# TODO: Add caching or specialized spatial search fields if needed later
class ReportFilter(django_filters.FilterSet):
    created_after = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.IsoDateTimeFilter(field_name='updated_at', lookup_expr='gt')

    class Meta:
        model = Report
        fields = {
            'status': ['exact', 'in'],
            'issue_type': ['exact', 'in'],
            'priority': ['exact', 'in'],
            'region': ['exact'],
            'submitted_by': ['exact'],
        }
