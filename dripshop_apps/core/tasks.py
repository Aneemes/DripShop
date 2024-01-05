#your_app/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task(name='send_email_task')
def send_email_task(title, message, send_to):
    """Send an email to the admin and the customer when an order is placed"""
    print("email sent")
    logger.info("Sent feedback email")
    return send_mail(title, message, settings.EMAIL_HOST_USER, [send_to], fail_silently=False)


