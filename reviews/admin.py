from django.contrib import admin
from .models import Review
from django.utils.html import format_html

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_approved', 'image_tag', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['name', 'email', 'comment']
    readonly_fields = ['created_at', 'image_tag']
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'location', 'rating', 'comment')
        }),
        ('Image', {
            'fields': ('image', 'image_tag')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_featured', 'display_location')
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Image'