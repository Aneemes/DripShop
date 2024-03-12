from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.models import Site
from dripshop_apps.core.utils import get_domain_name
from dripshop_apps.core.tasks import send_email_task
from dripshop_apps.notifications.models import Notification
#TODO:
#make this a celery task so its quicker 
#Make a model for admin_email and use that instead of settings.ADMIN_EMAIL so it is easier to chnage for the user
#also remove print statements amd format the email structure properly


def create_notification_on_order_placement(request, order):
    user = request.user
    title = 'order Placed'
    content = 'this is a content'
    notification = Notification.objects.create(user=user, title=title, content=content)

def send_mail_on_order_placement(request, order):
    """Send an email to the admin and the customer when an order is placed"""   
    domain = get_domain_name()
    transaction.on_commit(lambda: order_placed_mail_admin(request, order, domain))
    transaction.on_commit(lambda: order_placed_mail_customer(request, order, domain))

def order_placed_mail_admin(request, order, domain):
    """Send an email to the admin"""
   
    admin_url=order.get_admin_url()
    subject = 'New order Placed Successfully.'
    message = """The user {} has placed an order. 
    You can view your order details here: {}
    """.format(
        request.user.username,
        domain+admin_url
    )
    print(subject)
    print(message)
    
    # send_mail(subject, message, from_email=None, recipient_list=[ADMIN_EMAIL])
    # return send_email_task.apply_async(args=["New order placed by {}".format(request.user.username), message, settings.ADMIN_EMAIL])

def order_placed_mail_customer(request, order, domain):
    """Send an email to the customer"""

    print('email sent to customer')
    print(request.user.email)
    url=order.get_absolute_url()
    subject = 'Order Placed Successfully.'
    message = """Thank you for your order, {}. 
    You can track your order here: {}
    """.format(
        request.user.username,
        domain+url
    )
    # send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])
    print(subject)
    print(message)
    print("emailing is commented out")

    # func.delay() doesnt work so apply_async([])
    # return send_email_task.apply_async(args=["Your order has been placed successfully.", message, request.user.email])