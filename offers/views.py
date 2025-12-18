from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Offer
from .serializers import OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return Offer.objects.all()
        return Offer.objects.filter(status='active')
