from .base import *

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "testdb"}}

DEBUG = False

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False