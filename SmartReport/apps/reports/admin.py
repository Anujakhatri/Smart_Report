from django.contrib import admin
from apps.reports.models import Report, ReportImage, ReportCluster


class ReportImageInline(admin.TabularInline):
    model = ReportImage
    extra = 1
    # TODO: Add image thumbnail preview if required by the admin user interface


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_type', 'status', 'priority', 'submitted_by', 'region', 'created_at')
    list_filter = ('status', 'issue_type', 'priority')
    search_fields = ('title', 'description')
    inlines = [ReportImageInline]


@admin.register(ReportCluster)
class ReportClusterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('reports',)
