"""
Django settings for guyamoe project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import subprocess
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
PARENT_DIR = BASE_DIR.parent

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SECRET_KEY = os.environ.get("SECRET_KEY", "oxrdiDDsuMtd8SIsgAy7i+aJzSGCWt3Xl1IXeMyfCbA=")

CANONICAL_ROOT_DOMAIN = "youzitsu.ga"

ALLOWED_HOSTS = ["localhost","54.169.199.132","youzitsu.ga"]

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    "reader.apps.ReaderConfig",
    "homepage.apps.HomepageConfig",
    "misc.apps.MiscConfig",
    "user.apps.UserConfig",
    'admin_interface',
    'colorfield',
    "registration",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# INTERNAL_IPS = ("127.0.0.1",)

ROOT_URLCONF = "guyamoe.urls"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

MIDDLEWARE = [
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "homepage.middleware.ReferralMiddleware",
]

# REFERRAL_SERVICE = 'http://127.0.0.1:8080' # Change this to where-ever Ai is hosted

ROOT_URLCONF = "guyamoe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "guyamoe.context_processors.branding",
                "guyamoe.context_processors.home_branding",
                "guyamoe.context_processors.urls",
            ],
        },
    },
]

WSGI_APPLICATION = "guyamoe.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
]

# Registration

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
REGISTRATION_OPEN = False
INCLUDE_REGISTER_URL = True

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "vi"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_global"),
]

STATIC_VERSION = "?v=" + subprocess.check_output(
    ["git", "-C", str(BASE_DIR), "rev-parse", "--short", "HEAD"], text=True
)

MEDIA_URL = "/media/"

# IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID", "")
# MAIL_DISCORD_WEBHOOK_ID = int(os.environ.get("MAIL_DISCORD_WEBHOOK_ID", 1))
# MAIL_DISCORD_WEBHOOK_TOKEN = os.environ.get("MAIL_DISCORD_WEBHOOK_TOKEN", "")

BRANDING_NAME = "Youzitsu"
BRANDING_DESCRIPTION = "A place to read the entirety of the Kaguya-sama: Love is War manga. No ads. No bad reader. All guya."
BRANDING_IMAGE_URL = "https://i.imgur.com/jBhT5LV.png"

HOME_BRANDING_NAME = "Read the Kaguya-sama manga series | Youzitsu"
HOME_BRANDING_DESCRIPTION = "Read the Kaguya-sama: Love is War / Kaguya Wants to Be Confessed To manga and spin-off series. No ads. No bad reader. All guya."
HOME_BRANDING_IMAGE_URL = "https://i.imgur.com/jBhT5LV.png"

IMAGE_PROXY_URL = "https://proxy.f-ck.me"
