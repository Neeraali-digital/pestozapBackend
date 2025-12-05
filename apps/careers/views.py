from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'employment_type']
    search_fields = ['title', 'location']
    ordering_fields = ['created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_jobs = self.queryset.filter(status='active')
        serializer = self.get_serializer(active_jobs, many=True)
        return Response(serializer.data)


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['job']
    search_fields = ['full_name', 'email']
    ordering_fields = ['created_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
