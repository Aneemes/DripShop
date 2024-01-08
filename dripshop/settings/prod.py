from .base import *
 
DEBUG = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

SECRET_KEY = 'egfatgasgesgsegsedsdgsrghs-g-srgsd-gasegfseg'

DATABASES = {
    'default': {
        #---Postgres settings
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'PORT': os.environ.get('DB_PORT'),
    }
}