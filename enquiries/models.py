from django.db import models
from django.contrib.auth.models import User
import json

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in-progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    SERVICE_CHOICES = [
        ('single', 'Single Service'),
        ('3-services', '3 Services (1 Year)'),
        ('6-services', '6 Services (2 Years)'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('termite', 'Termite'),
        ('inspection', 'Inspection'),
        ('rodent', 'Rodent Control'),
    ]

    TYPE_CHOICES = [
        ('contact', 'Contact Message'),
        ('enquiry', 'Enquiry'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='enquiry')
    subject = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=100, blank=True, null=True) # Removed choices for flexibility
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields for enquiry form
    address = models.TextField(blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True) # Changed to CharField for ranges/text
    building_age = models.CharField(max_length=50, blank=True, null=True)
    pests = models.JSONField(blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)
    urgency = models.CharField(max_length=50, blank=True, null=True)
    preferred_time = models.CharField(max_length=100, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    
    # New fields from Rate Cards
    package_name = models.CharField(max_length=100, blank=True, null=True)
    quoted_price = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.customer_name}"
