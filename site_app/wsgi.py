"""WSGI config: what gunicorn serves (`gunicorn site_app.wsgi`)."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_app.settings')

application = get_wsgi_application()
