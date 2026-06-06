from rest_framework import serializers
from apps.regions.models import Province, District

class DistrictSerializer(serializers.ModelSerializer):
    province_id = serializers.UUIDField(source='province.id', read_only=True)
    province_name = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ['id', 'name', 'code', 'province_id', 'province_name']

    def get_province_name(self, obj):
        return obj.province.name


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code']


class ProvinceDetailSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'code', 'districts']
