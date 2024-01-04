#your_app/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from time import sleep

logger = get_task_logger(__name__)

@shared_task(name="add task")
def add(x,y):
    sum = x+y
    print(sum)
    print('a')
    return (x+y)

# @shared_task(name='send_email_to')
# def send_email_to(title, message, send_to):
#     """Send an email to the admin and the customer when an order is placed"""
#     logger.info("email sent")
#     return send_mail(title, message, settings.EMAIL_HOST_USER, [send_to])

@shared_task(name='send_email_to')
def send_email_to(title, message, send_to):
    """Send an email to the admin and the customer when an order is placed"""
    print("email sent")
    logger.info("Sent feedback email")
    return send_mail(title, message, settings.EMAIL_HOST_USER, [send_to], fail_silently=False)

# @task(name='send_email_task')
# def send_mail_task(subject, message, email_from, recepient_list):
#     msg = EmailMessage(subject, message, email_from, recepient_list)
#     msg.content_subtype = 'html'
#     msg.send()

