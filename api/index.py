import os
import sys

# Add your project path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gender_api'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gender_api.settings')

app = get_wsgi_application()