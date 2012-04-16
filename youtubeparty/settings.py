import os
import sys

FILEROOT = os.path.dirname(__file__)

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = True
USE_TZ = False

SITE_ID = 1

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(FILEROOT, 'media/')
# URL that handles the media served from MEDIA_ROOT
MEDIA_URL = '/media/'
# Absolute path to the directory static files should be collected to.
STATIC_ROOT = os.path.join(FILEROOT, 'static/')
# URL prefix for static files.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

#LOGIN_REDIRECT_URL=''

ROOT_URLCONF = 'youtubeparty.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'youtubeparty.wsgi.application'

TEMPLATE_DIRS = (
	os.path.join(FILEROOT, '..', 'templates'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'central',
	'tagging',
	'south',
	'bootstrap_toolkit',
	'django.contrib.admin',
	'guardian',
)

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1
LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages')

try:
	from local_settings import *
except ImportError:
	print "You need to create a local_settings.py file."
	print "You might want to `cp youtubeparty/local_settings.py{.example,}`"
	sys.exit(1)
