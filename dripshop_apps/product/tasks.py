import os
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from pyrebase import pyrebase

firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
storage = firebase.storage()

@shared_task(name='upload_to_firebase')
def upload_to_firebase(local_path, firebase_path, instance_type):
    # Upload to Firebase Storage
    storage.child(firebase_path).put(local_path)
    print(f"Uploaded {instance_type} to Firebase:", firebase_path)

