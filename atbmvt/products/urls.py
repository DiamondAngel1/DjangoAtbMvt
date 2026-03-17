from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('upload_temp_image/', views.upload_temp_image, name='upload_temp_image'),
    path('delete_temp_image/', views.delete_temp_image, name='delete_temp_image'),
]
