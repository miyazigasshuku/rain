from django.contrib import admin

# Register your models here.

from .models import Photo, Images

admin.site.register(Photo)
admin.site.register(Images)
