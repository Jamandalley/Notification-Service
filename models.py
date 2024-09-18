# notifications/models.py
from django.db import models
import uuid

class Admin(models.Model):
    admin_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __str__(self):
        return str(self.user_id)

class Provider(models.Model):
    provider_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    twilio_sid = models.CharField(max_length=64)
    twilio_auth_token = models.CharField(max_length=64)
    service_sid = models.CharField(max_length=64)
    admin_details = models.CharField(max_length=64)
    # admin= models.ForeignKey('Admin', on_delete=models.CASCADE, related_name='providers')

    def __str__(self):
        return str(self.provider_id)

class User(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    provider_id =  models.CharField(max_length=64)
    # provider = models.ForeignKey("Provider", on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def __str__(self):
        return str(self.user_id)

class AppConfiguration(models.Model):
    app_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_id = models.CharField(max_length=64)
    app_name = models.CharField(max_length=32)
    # provider = models.ForeignKey("Provider", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.app_id)

class Notification(models.Model):
    notification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # user = models.ForeignKey("User", on_delete=models.CASCADE)
    app_code = models.CharField(max_length=32)
    message = models.TextField()
    countryCode = models.CharField(max_length=15)
    mobileNumber = models.CharField(max_length=15)
    type = models.CharField(max_length=10)  # SMS or WhatsApp
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.notification_id)
