from django import forms
from django.db.models import fields

from .models import Photo, Image, Post


class UploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('user', 'photo')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'file')
