from django.urls import path
from .views import dashboard_stats

urlpatterns = [
    path('api/dashboard/stats/', dashboard_stats, name='dashboard_stats'),
]