from .settings import *  # noqa
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')sk1+b9wer_h4a8d#(gcfm63ycp1)l@mzf(k@v)ne-6n)n908&'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'charity',
        'USER': 'postgres',
        'PASSWORD': 'coderslab',
    }
}