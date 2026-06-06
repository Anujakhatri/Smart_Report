from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.regions.serializers import DistrictSerializer
from apps.reports.models import Report, ReportImage, ReportCluster

User = get_user_model()


class ReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportImage
        fields = ['id', 'image', 'uploaded_at']

    def validate_image(self, value):
        # Enforce max file size 10MB in serializer validation
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image file size cannot exceed 10MB.")
        return value

    def validate(self, attrs):
        # validates report image count <= 5
        report = attrs.get('report')
        # For updates/creates where report already exists
        if report and report.images.count() >= 5:
            raise serializers.ValidationError("A report can have a maximum of 5 images.")
        return attrs


class ReportListSerializer(serializers.ModelSerializer):
    submitted_by = serializers.CharField(source='submitted_by.username', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'issue_type', 'status', 'priority', 
            'latitude', 'longitude', 'submitted_by', 'created_at'
        ]


class ReportDetailSerializer(serializers.ModelSerializer):
    images = ReportImageSerializer(many=True, read_only=True)
    region = DistrictSerializer(read_only=True)
    submitted_by = serializers.CharField(source='submitted_by.username', read_only=True)
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'description', 'issue_type', 'status', 'priority',
            'latitude', 'longitude', 'region', 'submitted_by', 'assigned_to',
            'rejection_reason', 'images', 'created_at', 'updated_at', 'submitted_at'
        ]


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['issue_type', 'description', 'latitude', 'longitude', 'region']

    # TODO: Implement location bounding check if strict regional boundaries are enforced
    def validate(self, attrs):
        return attrs


class ReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['status', 'priority', 'assigned_to', 'rejection_reason']
        extra_kwargs = {
            'status': {'required': False},
            'priority': {'required': False},
            'assigned_to': {'required': False},
            'rejection_reason': {'required': False},
        }


class MapMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'issue_type', 'status', 'latitude', 'longitude', 'updated_at']


class ReportClusterSerializer(serializers.ModelSerializer):
    reports = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Report.objects.all(),
        required=False
    )
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = ReportCluster
        fields = ['id', 'name', 'description', 'reports', 'created_by', 'created_at']

    def create(self, validated_data):
        reports = validated_data.pop('reports', [])
        cluster = ReportCluster.objects.create(**validated_data)
        if reports:
            cluster.reports.set(reports)
        return cluster
