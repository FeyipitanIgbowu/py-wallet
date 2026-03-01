from django.conf import settings
from django.db import models



# Create your models here.

class Notification(models.Model):
    CHANNEL_TYPE = (
        ('email', 'Email'),
        ('sms', 'SMS'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reference = models.CharField(max_length=50, unique=True, blank=True, null=True)
    message = models.TextField()
    channel = models.CharField(max_length=50, choices=CHANNEL_TYPE, default='email')
    event_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
