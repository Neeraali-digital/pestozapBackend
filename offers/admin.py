from django.contrib import admin
from .models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'discount', 'discount_type', 'status', 'valid_from', 'valid_to']
    list_filter = ['status', 'discount_type', 'created_at']
    search_fields = ['title', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']