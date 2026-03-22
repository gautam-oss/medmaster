import os
from pathlib import Path
from .base import *

# ─────────────────────────────────────────────────────────────────────────────
# LOCAL DEVELOPMENT — WSL / SQLite / no .env file required
# Loads .env.local if it exists, otherwise uses safe hardcoded defaults.
# ─────────────────────────────────────────────────────────────────────────────

# Load .env.local automatically if it exists
_env_file = Path(__file__).resolve().parent.parent.parent / '.env.local'
if _env_file.exists():
    with open(_env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-dev-key-change-in-production-12345'
)
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# SQLite — zero setup, works out of the box
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'