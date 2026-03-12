from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
]