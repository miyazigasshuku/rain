from django.urls import path

from .import views

app_name = 'photoremake'
urlpatterns = [
    path('', views.index, name="index"),
    path('upload/', views.upload_photo, name="upload"),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('emotion/', views.emotion, name='emotion')
]
