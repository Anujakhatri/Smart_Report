from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ReportCreateSerializer,ReportListSerializer
from .models import Report

class ReportCreateView(generics.CreateAPIView):
    serializer_class = ReportCreateSerializer
    permission_classes =[IsAuthenticated]
    parser_classes =[MultiPartParser,FormParser]

    def perform_create(self,serializer):
        serializer.save(reporter=self.request.user)

class MyReportView(generics.ListAPIView):
    serializer_class = ReportListSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(reporter=self.request.user)

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        return HttpResponse(f"Hello, {name}!")

    return render(request, "home.html")