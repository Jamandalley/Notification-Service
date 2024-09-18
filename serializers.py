# notifications/serializers.py

from rest_framework import serializers
from .models import Provider, User, AppConfiguration, Notification, Admin
from django.contrib.auth.hashers import make_password

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['admin_id', 'name', 'password']
        read_only_fields = ['admin_id']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ProviderSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Provider
        fields = ['provider_id', 'twilio_sid', 'twilio_auth_token', 'service_sid', 'admin_details']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'password', 'provider_id']

class AppConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfiguration
        fields = ['app_id', 'user_id', 'app_name']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_id', 'app_code', 'message', 'countryCode', 'mobileNumber', 'type', 'sent_at']

class EmailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    attachment = serializers.FileField(required=False)
    template_name = serializers.CharField(max_length=255, required=False)

class TemplateUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    file = serializers.FileField()
