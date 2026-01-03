"""
Django settings for smart_repairer project.
"""

from pathlib import Path
import os  # ✅ Moved to top for cleaner code

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# 🚀 SECURITY & DEPLOYMENT SETTINGS
# ==========================================

# SECURITY WARNING: keep the secret key used in production secret!
# (It falls back to the insecure key if the environment variable isn't set)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-a!y1vy9(9ley3-ek62r@g=!d=ee2#l)r%6k_=_g0&j(zzn+^)(')

# SECURITY WARNING: don't run with debug turned on in production!
# ✅ This automatically detects if you are on Render. 
# If on Render -> DEBUG is False. If on Laptop -> DEBUG is True.
DEBUG = 'RENDER' not in os.environ

# ✅ Allow the app to run on Render's web address
ALLOWED_HOSTS = ['*']

# ✅ Fixes "CSRF Failed" errors on Render login pages
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',

    # Your apps
    'repair',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', # Optional: Add if using WhiteNoise later
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = 'smart_repairer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # ✅ Ensures Django finds your HTML files
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

WSGI_APPLICATION = 'smart_repairer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==========================================
# 📂 STATIC & MEDIA FILES
# ==========================================

STATIC_URL = 'static/'

# Where your local static files live (CSS/Images during development)
STATICFILES_DIRS = [BASE_DIR / 'repair' / 'static']

# ✅ Where Django collects files for Deployment (Critical for Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Files (User uploaded images like tire punctures)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
