from django.db import models
from django.conf import settings

class Report(models.Model):
    STATUS_CHOICES= [
        ('pending','Pending'),
        ('received','Received'),
        ('approved','Approved'),
        ('fixed','Fixed'),

    ]
    CATEGORY_CHOICES = [
    ('road', 'Road / Pothole'),
]

    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES,default='road'),
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    photo = models.ImageField(upload_to='photos/')
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    landmark = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')