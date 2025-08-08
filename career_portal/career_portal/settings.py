# career_portal/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv

# --- Basic Django Setup ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()  # Load environment variables from .env file

SECRET_KEY = 'django-insecure-=%u^y5f0831c!!-=_c!q1dm0ifhz-vh*=0c&d^p5d+8))axi5#'
DEBUG = True
ALLOWED_HOSTS = []


# --- Application Definition ---
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites', # This is often related to allauth, can be removed if not used elsewhere.
    'users',
    'internships',
    'applications',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # REMOVED: 'allauth.account.middleware.AccountMiddleware', # This was causing the error
]

ROOT_URLCONF = 'career_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'career_portal.wsgi.application'


# --- Database ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static and Media Files ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# --- Other Settings ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Email Configuration ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testing142701@gmail.com'
EMAIL_HOST_PASSWORD = 'sgzm mrhs fpfc qpcg'


# ==============================================================================
#   AUTHENTICATION CONFIGURATION
# ==============================================================================

# --- Custom User Model ---
AUTH_USER_MODEL = 'users.User'

# --- NEW Auth0 Configuration ---
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'users.auth0_backend.Auth0Backend',
]

# --- REMOVED all old 'django-allauth' settings ---
# SITE_ID, ACCOUNT_*, SOCIALACCOUNT_* settings have been removed as they are no longer needed.
LOGIN_URL = 'users:login'