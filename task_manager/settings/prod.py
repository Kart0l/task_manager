from dotenv import load_dotenv
import dj_database_url


from .base import *




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    os.environ.get('ALLOWED_HOST', 'localhost'),
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# add whitenoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# URL for connecting to Neon PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_seqtygkp5lF6@ep-lucky-frost-a2od4yqd-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require')

# Configuration via dj-database-url
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True