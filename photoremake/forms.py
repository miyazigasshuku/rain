from django import forms

from .models import Photo

class UploadForm(forms.ModelForm):

  class Meta:
    model = Photo
    fields = ('user', 'photo')