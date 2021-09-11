from core.settings import *

DEBUG = False
SECRET_KEY = 'very-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'accountant',
        'NAME': 'accountant_test',
        'PASSWORD': 'accountant',
        'HOST': 'localhost',
    },
}