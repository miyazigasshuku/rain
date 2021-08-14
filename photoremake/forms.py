from django import forms
from django.db.models import fields
from .models import Images, Photo


class UploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'photo')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('title', 'image', 'action', 'user',)