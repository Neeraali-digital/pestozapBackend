"""
URL configuration for pestozap_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/', include([
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),
        path('users/', include('apps.users.urls')),
        path('blog/', include('apps.blog.urls')),
        path('admin/', include('apps.blog.admin_urls')),
        path('enquiries/', include('enquiries.urls')),
        path('offers/', include('offers.urls')),
        path('reviews/', include('reviews.urls')),
        path('dashboard/', include('dashboard.urls')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)