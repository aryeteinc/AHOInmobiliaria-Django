
from pathlib import Path
import pymysql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar PyMySQL para que funcione como MySQLdb
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-2xf-@%llwnppp3la4%!q9ng%t*wwu@8)3-7#05)jsqlk$9j4!^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tinymce",  # Rich text editor
    "inmobiliaria.apps.InmobiliariaConfig",  # Asegúrate de que tu aplicación inmobiliaria esté registrada aquí
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
       # Crea una conexion a MySQL
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "inmuebles"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", "rootpassword"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Media files (uploaded files)
MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv("MEDIA_ROOT", "media"))

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# TinyMCE Configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        textcolor save link image media preview codesample contextmenu
        table code lists fullscreen  insertdatetime  nonbreaking
        contextmenu directionality searchreplace wordcount visualblocks
        visualchars code autolink lists  charmap print  hr
        anchor pagebreak
        ''',
    'toolbar1': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect  | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
        ''',
    'toolbar2': '''
        visualblocks visualchars |
        charmap hr pagebreak nonbreaking anchor |  code |
        ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

# Configuración específica para descripción corta (más simple)
TINYMCE_SIMPLE_CONFIG = {
    'height': 150,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': 'textcolor link lists',
    'toolbar': 'bold italic underline | forecolor | alignleft aligncenter alignright | bullist numlist | link',
    'menubar': False,
    'statusbar': False,
}
