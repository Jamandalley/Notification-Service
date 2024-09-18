from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Provider, User, AppConfiguration, Notification

admin.site.register(Provider)
admin.site.register(User)
admin.site.register(AppConfiguration)
admin.site.register(Notification)