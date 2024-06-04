

# Import Django environ and initialise environment variables

import environ

env = environ.Env()

environ.Env.read_env()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ['django-app-lfsl.onrender.com', '*']

CSRF_TRUSTED_ORIGINS = ['https://django-app-lfsl.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'account',
    'client',
    'writer',
    'storages',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_USER_MODEL = 'account.CustomUser'

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups' # This essentially allows pop ups from paypal

MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'subplatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'subplatform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# SQLite database (development - default)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'subplatform',
#         'HOST': '127.0.0.1',
#         'USER': 'elijah',
#         'PASSWORD': 'pass',
#         'PORT': '3306',
#     }
# }


# PostgreSQL database (production)

import dj_database_url

DATABASES = {
    
    'default': dj_database_url.parse(env('DATABASE_URL'))
    
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP Configuration


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # Use an App Password if 2FA is enabled
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


# Amazon S3 Configuration

# Enter your AWS Access key ID HERE
# Enter your AWS Secret Access key ID HERE
 
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME') # Enter your S3 bucket name HERE


STORAGES = {
    
    # Media file (image) management
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",  
    },
    
    # CSS and JS File management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False

# PayPal Credentials

SS_CLIENT_ID = env('SS_CLIENT_ID')
    
SS_SECRET_ID = env('SS_SECRET_ID')
