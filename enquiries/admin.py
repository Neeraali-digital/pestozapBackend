from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['subject', 'customer_name', 'email', 'service_type', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'service_type', 'created_at']
    search_fields = ['subject', 'customer_name', 'email']
    readonly_fields = ['created_at', 'updated_at']