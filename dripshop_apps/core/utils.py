from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site

def get_domain_name():
    domain_name = Site.objects.get_current().domain
    return domain_name

#as of now its for order emails
# TODO:use celery to send emails and change name to something specific
# def send_email_to(title,message, send_to):
#     """Send an email to the admin and the customer when an order is placed"""
#     send_mail(title, message, settings.EMAIL_HOST_USER, [send_to])
