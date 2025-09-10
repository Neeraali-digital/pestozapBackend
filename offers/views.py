from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Offer
from .serializers import OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'discount_type']
    search_fields = ['title', 'code', 'description']
    ordering_fields = ['created_at', 'valid_to']
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = self.queryset.count()
        active = self.queryset.filter(status='active').count()
        expired = self.queryset.filter(status='expired').count()
        total_usage = sum(offer.used_count for offer in self.queryset.all())
        
        return Response({
            'total': total,
            'active': active,
            'expired': expired,
            'total_usage': total_usage
        })
    
    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        offer = self.get_object()
        offer.status = 'active' if offer.status == 'inactive' else 'inactive'
        offer.save()
        return Response({'status': offer.status})