from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet

router = DefaultRouter()
router.register(r'', OfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]