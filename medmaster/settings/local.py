from .base import *

# ── Local dev — no .env file needed, just run and go ──────────────────────────

SECRET_KEY = 'django-insecure-local-dev-key-change-in-production-12345'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Show emails in terminal instead of sending them
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'