from django.db import models

class Offer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]
    
    DISCOUNT_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    usage_limit = models.IntegerField(default=100)
    used_count = models.IntegerField(default=0)
    services = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title