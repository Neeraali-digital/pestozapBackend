from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'employment_type', 'status', 'created_at')
    list_filter = ('status', 'employment_type')
    search_fields = ('title', 'location')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'created_at')
    list_filter = ('job',)
    search_fields = ('full_name', 'email')
