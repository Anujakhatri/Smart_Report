from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.regions.models import Province, District
from apps.regions.serializers import ProvinceSerializer, ProvinceDetailSerializer, DistrictSerializer

try:
    from core.pagination import CustomPagination
except ImportError:
    from rest_framework.pagination import PageNumberPagination
    class CustomPagination(PageNumberPagination):
        page_size = 10


class BaseResponseMixin:
    """
    Mixin to format all responses as {success: bool, data: {}, message: str}
    """
    def format_response(self, data, message="Success", success=True, status_code=status.HTTP_200_OK):
        return Response({
            "success": success,
            "data": data,
            "message": message
        }, status=status_code)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return self.format_response(
                data=paginated_response.data, 
                message="List retrieved successfully"
            )

        serializer = self.get_serializer(queryset, many=True)
        return self.format_response(
            data=serializer.data, 
            message="List retrieved successfully"
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.format_response(
            data=serializer.data, 
            message="Details retrieved successfully"
        )


class ProvinceViewSet(BaseResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProvinceDetailSerializer
        return ProvinceSerializer


class DistrictViewSet(BaseResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        province_id = self.request.query_params.get('province')
        if province_id:
            queryset = queryset.filter(province_id=province_id)
        return queryset
