from django.core.mail import send_mail
from config.celery import app
from celery import shared_task
from django.conf import settings


@shared_task
def send_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
