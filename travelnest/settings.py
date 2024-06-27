"""
Django settings for travelnest project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mb&oey%hnm5*v16mi$4t&4v3upx(41_g7o%2lk@oa3t68lpejl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
   
]


AUTH_USER_MODEL = 'app.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.RoleBasedAccessMiddleware', 
    # 'app.middleware.NoCacheMiddleware',
]

import logging

logger = logging.getLogger('django.security.csrf')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

ROOT_URLCONF = 'travelnest.urls'

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

WSGI_APPLICATION = 'travelnest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

import pymysql
pymysql.install_as_MySQLdb()
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'railway',
        # 'USER': 'root',
        # 'PASSWORD': 'YHSGYkCQnVmkMxhETGoFxmuwRFXjOyMe',
        # 'HOST': 'roundhouse.proxy.rlwy.net',
        # 'PORT': '23145',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('MYSQLDATABASE'),
        'USER': env('MYSQLUSER'),
        'PASSWORD': env('MYSQLPASSWORD'),
        'HOST': env('MYSQLHOST'),
        'PORT': env('MYSQLPORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-7fc2.up.railway.app',
                        
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "app/static"),
]
MEDIA_URL = '/images/'

MEDIA_ROOT = os.path.join(BASE_DIR,'app/static/images')
CORS_ALLOW_ALL_ORIGINS = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
JAZZMIN_SETTINGS = {
    # "site_title": "My Admin",
    # "site_header": "My Admin",
    # "welcome_sign": "Welcome to My Admin",
    "search_model": "app.User",
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["app.view_user"]},
        {"model": "app.User"},
        {"app": "app"},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["app", "app", "app.user"],
    "custom_links": {
        "app": [
            {"name": "User Role Stats", "url": "admin:user_role_stats", "icon": "fas fa-users"},
            {"name": "Hotel by Tinh", "url": "admin:hotel_by_tinh", "icon": "fas fa-hotel"},
            {"name": "Room by Hotel", "url": "admin:room_by_hotel", "icon": "fas fa-bed"},
            {"name": "Invoice by Month", "url": "admin:invoice_by_month", "icon": "fas fa-file-invoice"},
            {"name": "Revenue by Month", "url": "admin:revenue_by_month", "icon": "fas fa-dollar-sign"},
            {"name": "Hotel Rating", "url": "admin:hotel_rating", "icon": "fas fa-star"},
            {"name": "Current Promotions", "url": "admin:current_promotions", "icon": "fas fa-tags"},
        ]
    },
    # "custom_links": {
    #     "app": [
    #         {"name": "User Role Stats", "url": "admin:custom_user_role_stats", "icon": "fas fa-users"},
    #         {"name": "Hotel by Tinh", "url": "admin:custom_hotel_by_tinh", "icon": "fas fa-hotel"},
    #         {"name": "Room by Hotel", "url": "admin:custom_room_by_hotel", "icon": "fas fa-bed"},
    #         {"name": "Invoice by Month", "url": "admin:custom_invoice_by_month", "icon": "fas fa-file-invoice"},
    #         {"name": "Revenue by Month", "url": "admin:custom_revenue_by_month", "icon": "fas fa-dollar-sign"},
    #         {"name": "Hotel Rating", "url": "admin:custom_hotel_rating", "icon": "fas fa-star"},
    #         {"name": "Current Promotions", "url": "admin:custom_current_promotions", "icon": "fas fa-tags"},
    #     ]
    # },
    # # Customize which apps appear (tùy chọn)
    # 'navigation': [
    #     {'app': 'auth', 'model': 'user'},
    #     'app',  # Thay 'myapp' bằng tên ứng dụng của bạn
    # ],

    # # Customize which views appear (tùy chọn)
    # 'site_menu': [
    #     {'name': 'Dashboard', 'url': 'admin:index', 'permissions': ['app.view_user']},
    #     {'name': 'User Role Stats', 'url': 'admin:user_role_stats', 'permissions': ['app.view_user_role_stats']},
    #     {'name': 'Hotel By Tinh', 'url': 'admin:hotel_by_tinh', 'permissions': ['app.view_hotel_by_tinh']},
    #     {'name': 'Room By Hotel', 'url': 'admin:room_by_hotel', 'permissions': ['app.view_room_by_hotel']},
    #     {'name': 'Invoice By Month', 'url': 'admin:invoice_by_month', 'permissions': ['app.view_invoice_by_month']},
    #     {'name': 'Revenue By Month', 'url': 'admin:revenue_by_month', 'permissions': ['app.view_revenue_by_month']},
    #     {'name': 'Hotel Rating', 'url': 'admin:hotel_rating', 'permissions': ['app.view_hotel_rating']},
    #     {'name': 'Current Promotions', 'url': 'admin:current_promotions', 'permissions': ['app.view_current_promotions']},
    # ],
    "icons": {
        "auth": "fas fa-users-cog",
        "app.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

#payment
# VNPAY_RETURN_URL = 'http://localhost:8000/payment_return'
VNPAY_RETURN_URL = 'https://web-production-7fc2.up.railway.app/payment_return'
VNPAY_PAYMENT_URL ='https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
VNPAY_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/api/transaction'
VNPAY_TMN_CODE ='I1TDDTC5'
VNPAY_HASH_SECRET_KEY ='WYEK2R3W4FO4N5JJ9OEHJW64JYPKYXNF'
