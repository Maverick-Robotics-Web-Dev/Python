import os
from .settings import *

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': get_env_file('DB_HOST'),
        'PORT': get_env_file('DB_PORT'),
        'USER': get_env_file('DB_USER'),
        'PASSWORD': get_env_file('DB_PW'),
        'NAME': get_env_file('DB_NAME'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'
