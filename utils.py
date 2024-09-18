import boto3
from django.core.mail import EmailMessage
from django.conf import settings
from botocore.exceptions import NoCredentialsError
import os

s3 = boto3.client('s3',
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                  region_name=settings.AWS_S3_REGION_NAME)

def upload_to_s3(file, bucket_name, object_name=None):
    if object_name is None:
        object_name = file.name
    try:
        s3.upload_fileobj(file, bucket_name, object_name)
    except NoCredentialsError:
        return None
    return f'https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{object_name}'

def get_template_from_s3(template_name):
    try:
        s3_response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=template_name)
        return s3_response['Body'].read().decode('utf-8')
    except s3.exceptions.NoSuchKey:
        return None

def send_email_with_attachment(recipient, subject, message, attachment=None, template_name=None):
    if template_name:
        template = get_template_from_s3(template_name)
        if template:
            message = template.replace("{{ content }}", message)

    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient]
    )

    if attachment:
        email.attach(attachment.name, attachment.read(), attachment.content_type)

    email.send()
