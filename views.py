# notifications/views.py
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404
from .models import Provider, User, AppConfiguration, Notification, Admin
from .serializers import ProviderSerializer, UserSerializer, AppConfigurationSerializer, NotificationSerializer, AdminSerializer,\
    EmailSerializer, TemplateUploadSerializer
from twilio.rest import Client
import json
from django.contrib.auth.hashers import make_password
from .kafkaProducer import produce_message
from .kafkaConsumer import create_kafka_consumer
import asyncio
from .tasks import send_sms, send_whatsapp
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .utils import send_email_with_attachment, upload_to_s3
from django.conf import settings

@api_view(["GET"])
def notification_center(request, format=None):
    return Response(
        {
            "admin-registration": reverse("admin-register", request=request, format=format),
            "providers": reverse("provider-list", request=request, format=format),
            "users": reverse("user-list", request=request, format=format),
            "app-configurations": reverse("appconfiguration-list", request=request, format=format),
            "notification-services": reverse("notification-list", request=request, format=format),
            "email": reverse("send-email", request=request, format=format),
            "template": reverse("upload-template", request=request, format=format),
        }
    )
    
class ResponseModel:
    def __init__(self, is_successful, message, data=None):
        self.is_successful = is_successful
        self.message = message
        self.data = data

class AdminRegisterView(generics.ListCreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        admin_list = []
        for data in serializer.data:
            admin_id = data['admin_id']
            admin_data = {
                "Name": data['name'],
                "AdminID": str(admin_id).replace("-", "")
            }
            admin_list.append(admin_data)
            
        response = ResponseModel(is_successful=True, message="Admins retrieved successfully", data=admin_list)
        return Response(response.__dict__)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Hash the password
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()

            # Access data directly
            data = serializer.data
            admin_id = data['admin_id']
            admin_data = {
                "Name": data['name'],
                "AdminID": str(admin_id).replace("-", "")
            }

            response = ResponseModel(is_successful=True, message="Admin created successfully", data=[admin_data])
            return Response(response.__dict__, status=status.HTTP_201_CREATED)
        
        # Handle invalid data
        response = ResponseModel(is_successful=False, message="Admin creation failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)
    

class ProviderList(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        provider_list = []
        for data in serializer.data:
            provider_id = data['provider_id']
            provider_data = {
                "ProviderID": str(provider_id).replace("-", ""),
                "TwilioSID": data['twilio_sid'],
                "TwilioAuthToken": data['twilio_auth_token'],
                "ServiceSID": data['service_sid']
            }
            provider_list.append(provider_data)
        
        response = ResponseModel(is_successful=True, message="Providers retrieved successfully", data=provider_list)
        return Response(response.__dict__, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            provider_data = {
                "ProviderID": str(serializer.data['provider_id']).replace("-", ""),
                "TwilioSID": serializer.data['twilio_sid'],
                "TwilioAuthToken": serializer.data['twilio_auth_token'],
                "ServiceSID": serializer.data['service_sid']
            }
            response = ResponseModel(is_successful=True, message="Provider created successfully", data=[provider_data])
            return Response(response.__dict__, status=status.HTTP_201_CREATED)
        response = ResponseModel(is_successful=False, message="Provider creation failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk') 
        provider_id = self.kwargs.get('provider_id')
        provider = get_object_or_404(Provider, provider_id=provider_id)
        serializer = ProviderSerializer(provider)
        # Removing admin_details from the response
        provider_data = serializer.data
        provider_data.pop('admin_details', None)
        response = ResponseModel(is_successful=True, message="Provider retrieved successfully", data=[provider_data])
        return Response(response.__dict__)

    def update(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        provider_id = self.kwargs.get('provider_id')
        provider = get_object_or_404(Provider, provider_id=provider_id)

        # Assuming 'admin_details' is part of the incoming request data
        request_admin_details = request.data.get('admin_details')
        
        if provider.admin_details != request_admin_details:
            response = ResponseModel(is_successful=False, message="Unauthorized", data=[])
            return Response(response.__dict__, status=status.HTTP_403_FORBIDDEN)

        serializer = ProviderSerializer(provider, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            provider_data = {
                "ProviderID": str(serializer.data['provider_id']).replace("-", ""),
                "TwilioSID": serializer.data['twilio_sid'],
                "TwilioAuthToken": serializer.data['twilio_auth_token'],
                "ServiceSID": serializer.data['service_sid']
            }
            response = ResponseModel(is_successful=True, message="Provider updated successfully", data=[provider_data])
            return Response(response.__dict__)

        response = ResponseModel(is_successful=False, message="Provider update failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        provider = get_object_or_404(Provider, pk=pk)
        
       # Log the incoming request data for debugging
        print("Request content type:", request.content_type)
        print("Request body:", request.body)
        
        request_admin_details = request.data.get('admin_details')
        
        # Logging for debugging
        print(f"Provider admin_details: {provider.admin_details}")
        print(f"Request admin_details: {request_admin_details}")
        
        
        if provider.admin_details != request_admin_details:
            response = ResponseModel(is_successful=False, message="Unauthorized", data=[])
            return Response(response.__dict__, status=status.HTTP_403_FORBIDDEN)
        provider.delete()
        response = ResponseModel(is_successful=True, message="Provider deleted successfully", data=[])
        return Response(response.__dict__, status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data ={
                "UserID": str(serializer.data['user_id']).replace("-", ""),
                "Name": serializer.data['name'],
                "ProviderID": serializer.data['provider_id']
            }

            response = ResponseModel(is_successful=True, message="User created successfully", data=[user_data])
            return Response(response.__dict__, status=status.HTTP_201_CREATED)
        response = ResponseModel(is_successful=False, message="User creation failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        user_list = []
        for data in serializer.data:
            user_data ={
                "UserID": str(data['user_id']).replace("-", ""),
                "Name": data['name'],
                "ProviderID": data['provider_id']
            }
            user_list.append(user_data)
        
        response = ResponseModel(is_successful=True, message="Users retrieved successfully", data=user_list)
        return Response(response.__dict__)
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, user_id=user_id)
        serializer = UserSerializer(user)
        # Removing user_password from the response
        user_data = serializer.data
        user_data.pop('password', None)
        retrieved_data ={
            "UserID": str(user_data['user_id']).replace("-", ""),
            "Name": user_data['name'],
            "ProviderID": serializer.data['provider_id']
        }
        response = ResponseModel(is_successful=True, message="User retrieved successfully", data=retrieved_data)
        return Response(response.__dict__)
    
    def update(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        user_id = self.kwargs.get('user_id')
        current_user = get_object_or_404(User, user_id=user_id)
        entered_password = request.data.get('password')
        
        if entered_password is None:
            response = ResponseModel(is_successful=False, message="Password not provided", data=[])
            return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the entered password matches the hashed password in the database
        elif entered_password != current_user.password:
            response = ResponseModel(is_successful=False, message="Unauthorized", data=[])
            return Response(response.__dict__, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(current_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_user_data ={
                "UserID": serializer.data['user_id'],
                "Name": serializer.data['name'],
                "ProviderID": serializer.data['provider_id']
            }
            response = ResponseModel(is_successful=True, message="User updated successfully", data=[updated_user_data])
            return Response(response.__dict__)
        response = ResponseModel(is_successful=False, message="User update failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        user_id = self.kwargs.get('user_id')
        current_user = get_object_or_404(User, user_id=user_id)
        current_user.delete()
        response = ResponseModel(is_successful=True, message="User deleted successfully", data=[])
        return Response(response.__dict__, status=status.HTTP_204_NO_CONTENT)

class AppConfigurationList(generics.ListCreateAPIView):
    queryset = AppConfiguration.objects.all()
    serializer_class = AppConfigurationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            app_configuration = serializer.save()
            app_details ={
                "AppName": serializer.data['app_name'],
                "User": serializer.data['user_id'],
                "AppCode": serializer.data['app_id']
            }
            response = ResponseModel(is_successful=True, message="App configuration created successfully", data=[app_details])
            return Response(response.__dict__, status=status.HTTP_201_CREATED)
        response = ResponseModel(is_successful=False, message="App configuration creation failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        configuration_list = []
        for data in serializer.data:
            app_data= {
                "AppName": data['app_name'],
                "User": data['user_id'],
                "AppCode": str(data['app_id']).replace("-", "")
            }
            configuration_list.append(app_data)
            
        response = ResponseModel(is_successful=True, message="App configurations retrieved successfully", data=configuration_list)
        return Response(response.__dict__)

class AppConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppConfiguration.objects.all()
    serializer_class = AppConfigurationSerializer
    permission_classes = [AllowAny]
    lookup_field = 'app_id'

    def retrieve(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        app_id = self.kwargs.get('app_id')
        app = get_object_or_404(AppConfiguration, app_id=app_id)
        serializer = AppConfigurationSerializer(app)
        app_data = serializer.data
        retrieved_data ={
                "AppName": app_data['app_name'],
                "User": app_data['user_id'],
                "AppCode": str(app_data['app_id']).replace("-", "")
            }
        response = ResponseModel(is_successful=True, message="User retrieved successfully", data=retrieved_data)
        return Response(response.__dict__)
    
    def update(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        app_id = self.kwargs.get('app_id')
        app = get_object_or_404(AppConfiguration, app_id=app_id)
        
        if app.user_id != request.data.get('user_id'):
            response = ResponseModel(is_successful=False, message="Unauthorized", data=[])
            return Response(response.__dict__, status=status.HTTP_403_FORBIDDEN)
        serializer = AppConfigurationSerializer(app, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_app_data= {
                "AppName": serializer.data['app_name'],
                "AppCode": serializer.data['app_id'],
                "User": serializer.data['user_id']
            }
            
            response = ResponseModel(is_successful=True, message="App configuration updated successfully", data=[updated_app_data])
            return Response(response.__dict__)
        response = ResponseModel(is_successful=False, message="App update failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        app_id = self.kwargs.get('app_id')
        app = get_object_or_404(AppConfiguration, app_id=app_id)
        app.delete()
        response = ResponseModel(is_successful=True, message="Application deleted successfully", data=[])
        return Response(response.__dict__, status=status.HTTP_204_NO_CONTENT)


class NotificationViewSet(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = PageNumberPagination()
        paginator.page_size = 3
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)

        response = ResponseModel(
            is_successful=True, 
            message="Notifications record retrieved successfully", 
            data=serializer.data  # No need to wrap it in a list
        )
        return paginator.get_paginated_response(response.__dict__)
    
    def create(self, request, *args, **kwargs):
        app_code = request.data.get('app_code')
        user_id = get_object_or_404(AppConfiguration, app_id=app_code).user_id
        provider_id = get_object_or_404(User, user_id= user_id).provider_id
        provider = get_object_or_404(Provider, provider_id= provider_id)
        twilio_client = Client(provider.twilio_sid, provider.twilio_auth_token)
        
        countryCode = request.data.get('countryCode')
        mobileNumber = request.data.get('mobileNumber')
        message = request.data.get('message')
        
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()

            produce_message(countryCode, mobileNumber, message)
            
            consumer = create_kafka_consumer()
            
            try:
                while True:
                    message = consumer.poll(1.0)
                        
                    if message is None:
                        print("waiting...")
                    elif message.error():
                        print(f"ERROR: {message.error()}")
                    else: 
                        val = message.value().decode('utf-8')
                        print(val)
                        data = json.loads(val)
                        countryCode = data['country_code']
                        mobileNumber = data['mobile_number']
                        recipient = countryCode + mobileNumber
                        message = data['message']
                        sender = provider.service_sid
                        
                        if str(request.data['type']).upper() == 'SMS':
                            send_sms(twilio_client, sender, recipient, message)
                            response = ResponseModel(is_successful=True, message="Notification sent successfully", data=[serializer.data])
                            return Response(response.__dict__, status=status.HTTP_201_CREATED)
                        
                        elif str(request.data['type']).upper() == 'WHATSAPP':
                            send_whatsapp(twilio_client, sender, recipient, message)
                            response = ResponseModel(is_successful=True, message="Notification sent successfully", data=[serializer.data])
                            return Response(response.__dict__, status=status.HTTP_201_CREATED)
            except KeyboardInterrupt:
                    print("Consumption interrupted by user")
            finally:
                    consumer.close()            
        response = ResponseModel(is_successful=False, message="Notification sending failed", data=serializer.errors)
        return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)


class SendEmailView(generics.CreateAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            recipient = serializer.validated_data['recipient']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            attachment = request.FILES.get('attachment')
            template_name = serializer.validated_data.get('template_name')
            send_email_with_attachment(recipient, subject, message, attachment, template_name)
            return Response({'status': 'Email sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemplateUploadView(generics.CreateAPIView):
    serializer_class = TemplateUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['file']
            name = serializer.validated_data['name']
            file_url = upload_to_s3(file, settings.AWS_STORAGE_BUCKET_NAME, name)
            if file_url:
                return Response({'file_url': file_url}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Upload failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)