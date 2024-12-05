from os import getenv
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


load_dotenv(override=True, )


def replace_items(
    value: list[Any], replacements: list[tuple[str, str]] = [
        ("self", "'self'"),
        ("unsafe-eval", "'unsafe-eval'"),
        ("unsafe-inline", "'unsafe-inline'"),
    ]
) -> list[Any]:
    for index, item in enumerate(value):
        for old, new in replacements:
            if item != old:
                continue
            value[index] = new
            break
    return value


BASE_DIR = Path(__file__).resolve().parent.parent

SHARED_DIR = BASE_DIR / 'shared'

SECRET_KEY = getenv('DJANGO_SECRET_KEY')

DEBUG = getenv("DEBUG", 'False').lower() in ('true', '1')

ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1').split(',')

DJANGO_HOST = getenv('DJANGO_HOST', 'http://localhost:8000')

DJANGO_TELEGRAM_SECRET = getenv('DJANGO_TELEGRAM_SECRET')
DJANGO_TELEGRAM_USERNAME = getenv('DJANGO_TELEGRAM_USERNAME')

CSP_DEFAULT_SRC = replace_items(getenv('CSP_DEFAULT_SRC', '').split(','))
CSP_SCRIPT_SRC = replace_items(getenv('CSP_SCRIPT_SRC', '').split(','))
CSP_STYLE_SRC = replace_items(getenv('CSP_STYLE_SRC', '').split(','))
CSP_FONT_SRC = replace_items(getenv('CSP_FONT_SRC', '').split(','))
CSP_FRAME_ANCESTORS = replace_items(
    getenv("CSP_FRAME_ANCESTORS", "").split(",")
)
CSP_FRAME_SRC = replace_items(getenv("CSP_FRAME_SRC", "").split(","))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.telegram',
    "csp",

    'user.apps.UserConfig',
    'tgauth.apps.TgAuthConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': SHARED_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

AUTH_USER_MODEL = "user.User"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LANGUAGE_CODE = getenv('LANGUAGE_CODE', 'en-us')

TIME_ZONE = getenv('TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = SHARED_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIALACCOUNT_PROVIDERS = {
    'telegram': {
        'APP': {
            'client_id': getenv('DJANGO_TELEGRAM_UID'),
            'secret': getenv('DJANGO_TELEGRAM_SECRET'),
        },
        'AUTH_PARAMS': {'auth_date_validity': 60},
    }
}

LOGIN_URL = 'tgauth-login'

LOGIN_REDIRECT_URL = 'tgauth-profile'

LOGOUT_REDIRECT_URL = 'tgauth-index'
