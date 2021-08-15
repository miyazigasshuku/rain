from django.urls import path

from .import views

app_name = 'photoremake'
urlpatterns = [
    path('', views.index, name="index"),
    path('<pk>/update', views.PhotoUpdateView.as_view(), name='photo-update'),
    path('<pk>/delete', views.PhotoDeleteView.as_view(), name='photo-delete'),
    path('upload/', views.upload_photo, name="upload"),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('<pk>/emotion/', views.emotion, name='emotion')
]
