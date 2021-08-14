from django.contrib import admin

# Register your models here.

from .models import Photo, Back, Coordinated

admin.site.register(Photo)
admin.site.register(Back)
admin.site.register(Coordinated)