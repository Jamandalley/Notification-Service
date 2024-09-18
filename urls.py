# notifications/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProviderList, ProviderDetail, UserList, UserDetail, AppConfigurationList, AppConfigurationDetail, \
    NotificationViewSet, AdminRegisterView, notification_center, SendEmailView, TemplateUploadView

router = DefaultRouter()
# router.register(r'providers', ProviderList.as_view(), basename='provider')
# router.register(r'users', UserList.as_view(), basename='user')
# router.register(r'app-configurations', AppConfigurationList.as_view(), basename='appconfiguration')
# # router.register(r'notifications', NotificationViewSet, basename='notification')


urlpatterns = [
    path('', notification_center, name='api-root'),
    path('api/admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('providers/', ProviderList.as_view(), name='provider-list'),
    # path('providers/<int:pk>/', ProviderDetail.as_view(), name='provider-detail'),
    path('providers/<str:provider_id>/', ProviderDetail.as_view(), name='provider-detail'),
    path('users/', UserList.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<str:user_id>/', UserDetail.as_view(), name='user-detail'),
    path('app-configurations/', AppConfigurationList.as_view(), name='appconfiguration-list'),
    # path('app-configurations/<int:pk>/', AppConfigurationDetail.as_view(), name='appconfiguration-detail'),
    path('app-configurations/<str:app_id>/', AppConfigurationDetail.as_view(), name='appconfiguration-detail'),
    path('notifications/', NotificationViewSet.as_view(), name='notification-list'),
    path('send-email/', SendEmailView.as_view(), name='send-email'),
    path('upload-template/', TemplateUploadView.as_view(), name='upload-template'),
    path('', include(router.urls)),
]
