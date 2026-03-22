import os
from pathlib import Path
from .base import *

# ─────────────────────────────────────────────────────────────────────────────
# PRODUCTION — Docker Compose + AWS EC2
# All secrets come from environment variables (set via .env.production or
# directly on the EC2 instance). Hard fails on missing required values.
# ─────────────────────────────────────────────────────────────────────────────

# Load .env.production automatically if it exists (Docker Compose also injects
# these via env_file: .env.production in docker-compose.yml)
_env_file = Path(__file__).resolve().parent.parent.parent / '.env.production'
if _env_file.exists():
    with open(_env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())

SECRET_KEY = os.environ['SECRET_KEY']           # hard fail if missing
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ['DB_NAME'],
        'USER':     os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST':     os.environ.get('DB_HOST', 'db'),
        'PORT':     os.environ.get('DB_PORT', '5432'),
    }
}

# Security hardening
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True