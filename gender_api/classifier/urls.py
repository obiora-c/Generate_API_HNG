from django.urls import path
from .views import classify_name

urlpatterns = [
    path('api/classify', classify_name)
    
]
