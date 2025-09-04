"""
Admin configuration for the users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the User model.
    """
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'is_verified', 'is_staff', 'date_joined'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active',
        'is_verified', 'date_joined'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'phone_number', 'address', 'date_of_birth',
                'profile_picture', 'is_verified'
            )
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'email', 'first_name', 'last_name',
                'phone_number'
            )
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('profile')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserProfile model.
    """
    list_display = (
        'user', 'company', 'location',
        'email_notifications', 'created_at'
    )
    list_filter = (
        'email_notifications', 'sms_notifications',
        'marketing_emails', 'created_at'
    )
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'company')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'website', 'company', 'location')
        }),
        ('Preferences', {
            'fields': (
                'email_notifications', 'sms_notifications',
                'marketing_emails'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )