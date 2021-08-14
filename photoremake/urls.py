from django.urls import path

from .import views

app_name = 'photoremake'
urlpatterns = [
    path('', views.index, name="index"),
    path('upload/', views.upload_photo, name="upload"),
    path('coordinate/<int:pk>', views.coordinate, name="coordinate"),
    path('after/<int:pk>', views.after, name="after"),
    path('itiran/',views.MemberList.as_view(),name="itiran"),
    path('kozin/',views.IndividualList.as_view(), name="kozin"),
]