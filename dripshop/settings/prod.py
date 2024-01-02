from .base import *  

DATABASES = {
    'default': {
        #---Postgres settings
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dripshop',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'PORT': '5432',
    }
}