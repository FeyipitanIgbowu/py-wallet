from django.conf import settings
from django.db import models
# Create your models here.

class Notification(models.Model):
    CHANNEL_TYPE = (
        ('email', 'Email'),
        ('sms', 'SMS'),
    )
    wallet_number = models.CharField(max_length=100, blank=True, null=True)
    reference = models.CharField(max_length=50, unique=True, blank=True, null=True)
    message = models.TextField()
    channel = models.CharField(max_length=50, choices=CHANNEL_TYPE, default='email')
    event_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
