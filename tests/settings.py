import os.path
from django import VERSION

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'generic_confirmation',
)

MIDDLEWARE_CLASSES = MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SITE_ID = 1
SECRET_KEY = '+zzix-&k$afk-k0d0s7v01w0&15z#ne$71qf28#e$$c*@g742z'

ROOT_URLCONF = "urls"

DEBUG = False

LANGUAGE = "en-us"

STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'database.sqlite'),
    }
}

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


# prevent migrations from running during tests, because test models have none
if VERSION < (1,9):
    MIGRATION_MODULES = {
        'auth': 'tests.migrations.auth',
        'contenttypes': 'tests.migrations.contenttypes',
        'admin': 'tests.migrations.admin',
        'sessions': 'tests.migrations.sessions',
        'generic_confirmation': 'tests.migrations.generic_confirmation',
    }
else:
    MIGRATION_MODULES = {
        'auth': None,
        'contenttypes': None,
        'admin': None,
        'sessions': None,
        'generic_confirmation': None,
    }
