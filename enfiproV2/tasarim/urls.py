# tasarim/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasarim_anasayfa, name='tasarim_anasayfa'),  # Ana sayfa URL'si
    path('olustur/', views.tasarim_olustur, name='tasarim_olustur'),
    path('liste/', views.tasarim_listesi, name='tasarim_listesi'),
]