from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = open(BASE_DIR / 'wsgi/config/secret.txt').read().strip()

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'user_service.wsgi.urls'

WSGI_APPLICATION = 'user_service.wsgi.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
