"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$-p-x5&eif3cjfwv+jfksjd#jwr60eb2er8*mcwj6&-h-$4@#p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# # # ALLOWED_HOSTS = [u'192.168.3.60',]
# ALLOWED_HOSTS = [u'192.168.0.109',
#                  u'zdl.free.idcfengye.com',
#                  u'zzz.vipgz1.idcfengye.com',
#                  ]

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'corsheaders',

    # 'easy_thumbnails',
    # 'filer',
    # 'mptt',
    # 'taggit',
    'boards',
    'accounts',
    'record',
    'netdisk',
    'tasklist',
    'charge_record',
    # 'filemanager',
    # 'linkedcare',
    # 'api-utils',
	'rest_framework',
	'rest_framework.authtoken',
    'baseinfo',
	'summary',
	'appointment',
	'search',
	'testapp',
	'storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'corsheaders.middleware.CorsMiddleware',

]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 # os.path.join(BASE_DIR, 'vue-admin-template/dist'),
				os.path.join(BASE_DIR, 'vue-element/dist'),
                 ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'


# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = ("/static/")
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
	os.path.join(BASE_DIR, 'vue-admin-template/dist/static'),
	os.path.join(BASE_DIR, 'vue-element/dist/static'),

	# '/Users/Wang/static',
]

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'home2'


# api-设置
REST_FRAMEWORK = {
	# 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
	'DEFAULT_PAGINATION_CLASS': 'api_utils.custom_pagination.UserPagination',
	'PAGE_SIZE': 10,
	'EXCEPTION_HANDLER': 'api_utils.custom_exception.custom_exception_handler',
}

# CORS-跨域访问
CORS_ORIGIN_WHITELIST = [
	'http://localhost:8000',
	'http://192.168.11.17:8001',
	'http://localhost:8001',
	'http://localhost:8000',
]
CORS_ALLOW_CREDENTIALS = True  # 指明在跨域访问中，后端是否支持对cookie的操作。

