from rest_framework import serializers
from .models import Report


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["latitude", "longitude", "landmark", "photo", "category"]

class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "latitude", "longitude", "landmark", 
                  "photo", "category", "status", "created_at"]