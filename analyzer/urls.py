# analyzer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_code, name='analyze_code'),
]
