from .common import *
import django_heroku
import urllib.parse as urlparse
import os



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

django_heroku.settings(locals(), logging=False)

url = urlparse.urlparse(os.environ["DATABASE_URL"])

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": url.path[1:],
        "USER": url.username,
        "PASSWORD": url.password,
        "HOST": url.hostname,
        "PORT": url.port,
    }
}