import os
from django.core.wsgi import get_wsgi_application

# Production WSGI — Docker sets DJANGO_SETTINGS_MODULE via environment.
# Falls back to production settings if not set.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medmaster.settings.production')
application = get_wsgi_application()
app = application