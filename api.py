# api.py
import os
import django
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
application = get_wsgi_application()

def app(environ, start_response):
    return application(environ, start_response)