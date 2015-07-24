"""
Django settings for selclsos project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0zqx_%+)je_pdfvc0&3vtot25umuih-b9&ur=4k!n@f_1ypv%c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '*',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classes',
    'master',
    'news',
    'student',
    'bootstrap3',
    'xlrd',
    'DjangoUeditor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.staticfiles.finders.FileSystemFinder',
)

ROOT_URLCONF = 'selclsos.urls'

WSGI_APPLICATION = 'selclsos.wsgi.application'

# the path store the users' upload files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REPORT_CONTENT_TYPE = ('application/pdf',)
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
        'NAME': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# STATIC_ROOT =  os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)


# DEFAULT_FILE_STORAGE = '/files/upload/'

#MEDIA_URL = ''


# FILE_CHARSET='utf-8'
# DEFAULT_CHARSET='utf-8'

# AUTH_USER_MODEL = "student.Student"
UEDITOR_SETTINGS={
                 "images_upload":{
                     "allow_type":"jpg,png",
                    "path":"uploadimg",
                    "max_size":"2222kb"        #
                },
                 "files_upload":{
                      "allow_type":"zip,rar,pdf",
                     "path":"files" ,
                     "max_size":"2222kb"
                 },
                 "image_manager":{
                      "path":"",
                },
             }
