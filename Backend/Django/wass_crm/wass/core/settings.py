"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from unipath import Path
from locale import setlocale, LC_ALL

from tools.methods.core import get_env_file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).ancestor(2)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-vq7kf(&%sjouqb_=h52e(ra!0_pk!pssz#n+c$73is(we#s8kr'
SECRET_KEY = get_env_file('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = []

THIRD_APPS = [
    # 'django_filters',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',   # To revoke tokens
    'rest_framework_simplejwt',  # Rest with jwt
    'coreapi',  # To document the application
    'drf_yasg',  # To document the application
    'corsheaders'  # To add cors in the header
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

###### Custom Settings #########

setlocale(LC_ALL, 'es')
DATETIME_FORMAT = '%B %d, %Y - %H:%M:%S'
DATETIME_INPUT_FORMATS = ['%B %d, %Y - %H:%M:%S', '%d-%m-%Y - %H:%M:%S']
DATE_FORMAT = '%B %d, %Y'
DATE_INPUT_FORMATS = ['%B %d, %Y', '%d-%m-%Y']
TIME_FORMAT = '%H:%M:%S'
TIME_INPUT_FORMATS = ['%H:%M:%S', '%H:%M']
# AUTH_USER_MODEL = 'user_employee.UserEmployeeModel'
# LOGIN_URL = '/rest-api/v1/routes/business/vouchertype'
HOME_URL = '/'

CACV_KEY = {
    'USE_JWT': True,
    # 'LOGIN_SERIALIZER': 'apps.auth.serializers.LoginSerializer',
    # 'JWT_SERIALIZER': 'apps.auth.serializers.JWTSerializer',
    # 'JWT_SERIALIZER_WITH_EXPIRATION': 'apps.auth.serializers.JWTSerializerWithExpiration',
    # 'JWT_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'JWT_AUTH_COOKIE': 'jwt-cacv-auth-token',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-cacv-refresh-token',
    'JWT_AUTH_REFRESH_COOKIE_PATH': '/',
    'JWT_AUTH_SAMESITE': 'Lax',
    'JWT_AUTH_COOKIE_DOMAIN': None,
    'JWT_AUTH_SECURE': False,
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_RETURN_EXPIRATION': False,

    # 'TOKEN_SERIALIZER': 'apps.auth.serializers.TokenSerializer',
    # 'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
    # 'TOKEN_CREATOR': 'apps.support.default_create_token',
    'SESSION_LOGIN': True,
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    # To activate JWT
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
    'DATETIME_FORMAT': '%B %d, %Y - %H:%M:%S',
    'DATETIME_INPUT_FORMATS': ['%B %d, %Y - %H:%M:%S', '%d-%m-%Y - %H:%M:%S'],
    'DATE_FORMAT': '%B %d, %Y',
    'DATE_INPUT_FORMATS': ['%B %d, %Y', '%d-%m-%Y'],
    'TIME_FORMAT': '%H:%M:%S',
    'TIME_INPUT_FORMATS': ['%H:%M:%S']
    # The default permission policy may be set globally
    # 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated']

}

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'SIGNING_KEY': env('SIMPLE_JWT_SIGNING_KEY', default=None) or SECRET_KEY,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    # 'TOKEN_OBTAIN_SERIALIZER': 'restapi.users.serializers.CustomJwtToken'
}

# INTERNAL_IPS = [
#     "127.0.0.1"
# ]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:4200",
]
