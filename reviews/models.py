from django.db import models

class Review(models.Model):
    DISPLAY_LOCATION_CHOICES = [
        ('home', 'Home Page'),
        ('community', 'Community Page'),
        ('both', 'Both Pages'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_location = models.CharField(max_length=20, choices=DISPLAY_LOCATION_CHOICES, default='both')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"