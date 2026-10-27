"""
Django on Master da Web serverless. Everything comes from the project's
variables: DATABASE_URL (the database binding), AWS_* (the bucket binding),
DJANGO_SECRET_KEY (generated when the template was deployed).
"""
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'
# Generated when the template was deployed. The build runs collectstatic
# without the project's variables: a placeholder there (or in DEBUG), never
# when serving.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    if not (DEBUG or 'collectstatic' in sys.argv):
        raise ImproperlyConfigured('DJANGO_SECRET_KEY is empty: set it in the project variables.')
    SECRET_KEY = 'placeholder-for-the-build-only'

# The platform routes to this service only its own hosts (its address and
# the domains you add), so any Host it receives is one of them.
ALLOWED_HOSTS = ['*']
# HTTPS ends at the platform's edge.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'uploads',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'site_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'site_app.wsgi.application'

# The database binding's DATABASE_URL goes through the pooler, in
# transaction mode: no server-side cursors. (SQLite only where there is no
# database, as during the build.)
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "build.sqlite3"}',
        conn_max_age=60,
        conn_health_checks=True,
    )
}
DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en'
LANGUAGES = [('en', 'English'), ('pt-br', 'Português')]
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Uploaded files: the bucket (django-storages, with the binding's AWS_*
# names). Public bucket: plain links at its public address, no signing.
# Static files (the admin's CSS): collected at build, served by WhiteNoise.
_public = urlparse(os.environ.get('AWS_URL', ''))
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'bucket_name': os.environ.get('AWS_BUCKET', ''),
            'endpoint_url': os.environ.get('AWS_ENDPOINT') or None,
            'region_name': os.environ.get('AWS_DEFAULT_REGION') or 'auto',
            'access_key': os.environ.get('AWS_ACCESS_KEY_ID'),
            'secret_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'addressing_style': 'path' if os.environ.get('AWS_USE_PATH_STYLE_ENDPOINT') == 'true' else 'auto',
            'signature_version': 's3v4',
            'default_acl': None,
            'file_overwrite': False,
            'querystring_auth': not _public.netloc,
            'custom_domain': (_public.netloc + _public.path.rstrip('/')) or None,
            'url_protocol': f'{_public.scheme}:' if _public.scheme else 'https:',
        },
    },
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logs to the console: the platform collects them.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
