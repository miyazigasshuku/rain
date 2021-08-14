from django import forms
from django.db.models import fields

from .models import Coordinated, Photo

class UploadForm(forms.ModelForm):

  class Meta:
    model = Photo
    fields = ('user', 'photo')


class CoordinateForm(forms.ModelForm):
    class Meta:
        model = Coordinated
        fields = ('back_id', 'title')