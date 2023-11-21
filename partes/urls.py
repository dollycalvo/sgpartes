from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('ayuda', views.ayuda, name='ayuda')
    
]