import django_filters
from apps.reports.models import Report


class ReportFilter(django_filters.FilterSet):
    created_after = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.IsoDateTimeFilter(field_name='updated_at', lookup_expr='gt')

    # Dashboard-friendly aliases
    district = django_filters.NumberFilter(field_name='region', lookup_expr='exact')
    severity = django_filters.CharFilter(field_name='priority', lookup_expr='exact')
    date_from = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Report
        fields = {
            'status': ['exact', 'in'],
            'issue_type': ['exact', 'in'],
            'priority': ['exact', 'in'],
            'region': ['exact'],
            'submitted_by': ['exact'],
        }

