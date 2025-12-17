from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Enquiry
from .serializers import EnquirySerializer

class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'service_type', 'type']
    search_fields = ['subject', 'customer_name', 'email']
    ordering_fields = ['created_at', 'priority']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = self.queryset.count()
        new = self.queryset.filter(status='new').count()
        in_progress = self.queryset.filter(status='in-progress').count()
        resolved = self.queryset.filter(status='resolved').count()
        
        return Response({
            'total': total,
            'new': new,
            'in_progress': in_progress,
            'resolved': resolved
        })