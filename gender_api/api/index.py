import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add BOTH root and project folder
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "gender_api"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gender_api.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()