from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('my-profile/', views.my_profile_view, name='my-profile'),
]
