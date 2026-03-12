from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'categories'

urlpatterns = [
    path('create/', views.create_category, name='create_category'),
    path('', views.category_list, name='category_list'),
]