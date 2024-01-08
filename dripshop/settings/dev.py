from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'egfatgasgesgsegsedsdgsrghs-g-srgsd-gasegfseg'

DATABASES = {
    'default': {
        #---Postgres settings
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST':os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}