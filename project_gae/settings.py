# -*- coding: utf-8
"""
Project's settings.
"""
import os
import django

# Own constants
# -----------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT)
DJANGO_ROOT = os.path.dirname(django.__file__)

# Shortcuts
# -----------------------------------------------------------------------------
path = lambda *a: os.path.join(*a)
project_path = lambda *a: os.path.join(PROJECT_ROOT, *a)
django_path = lambda *a: os.path.join(DJANGO_ROOT, *a)

# Debugging
# -----------------------------------------------------------------------------
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Administrators
# -----------------------------------------------------------------------------
ADMINS = (('Admin', 'admin@foo.bar'),)
MANAGERS = ADMINS

# Databases
# -----------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '', 
        'USER': '', 
        'PASSWORD': '',
        'HOST': '', 
        'PORT': '', 
    }
}

# I18N - L10N
# -----------------------------------------------------------------------------
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Site
# -----------------------------------------------------------------------------
SITE_ID = 1

# Site media
# -----------------------------------------------------------------------------
MEDIA_ROOT = project_path('public', 'media')
MEDIA_URL = '/media/'

# Secret Key
# -----------------------------------------------------------------------------
SECRET_KEY = 'MUST-BE-SECRET'

# Templates
# -----------------------------------------------------------------------------
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
)

TEMPLATE_DIRS = (
    project_path('templates'),
)

# Middleware
# -----------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

# URLs
# -----------------------------------------------------------------------------
ROOT_URLCONF = '%s.urls' % PROJECT_NAME

# Caching
# -----------------------------------------------------------------------------
CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX = '%s_' % PROJECT_NAME

# Applications
# -----------------------------------------------------------------------------
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
)
