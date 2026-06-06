from django.contrib import admin
from apps.regions.models import Province, District

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'province')
    list_filter = ('province',)
    search_fields = ('name',)
