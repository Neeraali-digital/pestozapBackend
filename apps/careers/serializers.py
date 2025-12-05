from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('created_at',)
