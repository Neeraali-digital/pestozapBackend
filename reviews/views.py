from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rating', 'is_approved']
    search_fields = ['name', 'comment']
    ordering_fields = ['created_at', 'rating']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        display_location = self.request.query_params.get('display_location', None)
        if display_location:
            queryset = queryset.filter(display_location__in=[display_location, 'both'])
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        reviews = self.queryset.filter(is_approved=True)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        total_reviews = reviews.count()
        
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[f'{i}_star'] = reviews.filter(rating=i).count()
        
        return Response({
            'average_rating': round(avg_rating, 1),
            'total_reviews': total_reviews,
            'rating_distribution': rating_distribution
        })