from django.urls import path

from .import views

app_name = 'photoremake'
urlpatterns = [
    path('', views.index, name="index"),
    path('upload/', views.upload_photo, name="upload"),
]
