import os
from django.utils import timezone
from .tasks import upload_to_firebase
from django.conf import settings
from pyrebase import pyrebase

firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
storage = firebase.storage()


def sanitize_for_directory_name(value):
    # Replace spaces with underscores and remove other characters
    return ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in value)

def product_image_upload_path(instance, filename):
    title = getattr(instance.product, 'title', 'unknown')
    product_title = sanitize_for_directory_name(title)

    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    extension = os.path.splitext(filename)[1]
    local_path = f'uploads/products/{product_title}/general/{timestamp}{extension}'
    firebase_path = f'products/{product_title}/general/{timestamp}{extension}'

    # Ensure the local directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Save the file to the local directory
    with open(local_path, 'wb') as f:
        f.write(instance.image.read())

    # Use Celery to upload to Firebase Storage asynchronously
    upload_to_firebase.delay(local_path, firebase_path, 'Image')
    return local_path

def product_thumbnail_upload_path(instance, filename):
    title = getattr(instance, 'title', 'unknown')
    product_title = sanitize_for_directory_name(title)

    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    extension = os.path.splitext(filename)[1]
    local_path = f'uploads/products/{product_title}/thumbnail/{timestamp}{extension}'
    firebase_path = f'products/{product_title}/thumbnail/{timestamp}{extension}'

    # Ensure the local directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Save the file to the local directory
    with open(local_path, 'wb') as f:
        f.write(instance.thumbnail.read())

    # Use Celery to upload to Firebase Storage asynchronously
    upload_to_firebase.delay(local_path, firebase_path, 'Thumbnail')
    return local_path