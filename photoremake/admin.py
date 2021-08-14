from django.contrib import admin

# Register your models here.

from .models import Photo, Image

admin.site.register(Photo)
admin.site.register(Image)
