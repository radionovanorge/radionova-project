"""
Django settings for project project.

"""
import os
import sys
from distutils.util import strtobool
from pathlib import Path
import dotenv

dotenv.load_dotenv(".env.prod")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Application definition
INSTALLED_APPS = [
    "radionova.apps.RadionovaConfig",
    "rest_framework",
    "drf_yasg",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "corsheaders",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", default="radionova"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", default="127.0.0.1"),
        "PORT": int(os.environ.get("POSTGRES_PORT", default=5432)),
    }
}

# if 'test' in sys.argv or 'test_coverage' in sys.argv:
#     DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = os.environ.get("STATIC_URL", default="/static/")
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get("STATIC_ROOT", default="static"))

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "radionova.error_handling.custom_exception_handler",
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
    "USE_SESSION_AUTH": False,
}

CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", default=False)
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", default=False)
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", default="#um2g($a1-#2d(enmn!3pmg6axus*wbip_y#p!ezs0*$)(^!^o"
)
ENV_ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS")
ALLOWED_HOSTS = ENV_ALLOWED_HOSTS.split(",") if ENV_ALLOWED_HOSTS is not None else [
    'radionovaapi.azurewebsites.net',
]
DEBUG = bool(strtobool(os.environ.get("DEBUG", default="True")))

CORS_ALLOWED_ORIGINS = [
    "https://ashy-ocean-0cf36cb03.2.azurestaticapps.net",
]
