from django.urls import path

from .import views

app_name = 'photoremake'
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('upload/', views.upload_photo, name="upload"),
]
