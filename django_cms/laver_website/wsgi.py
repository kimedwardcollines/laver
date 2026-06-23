"""
WSGI config for Laver Website project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laver_website.settings')
application = get_wsgi_application()
