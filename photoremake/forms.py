from django import forms
from django.db.models import fields
from .models import Image, Photo

class UploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('user', 'photo', 'title')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image', 'action', 'user',)