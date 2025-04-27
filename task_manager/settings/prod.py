from dotenv import load_dotenv


from .base import *




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    os.environ.get('ALLOWED_HOST', 'localhost'),
]

# Додаємо whitenoise для статичних файлів
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
 'default': {
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': os.environ.get('DB_NAME', ''),
   'USER': os.environ.get('DB_USER', ''),
   'PASSWORD': os.environ.get('DB_PASSWORD', ''),
   'HOST': os.environ.get('DB_HOST', 'localhost'),
   'PORT': os.environ.get('DB_PORT', '5432'),
   'OPTIONS': {
     'sslmode': 'require',
   },
 }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True