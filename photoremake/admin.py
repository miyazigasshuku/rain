from django.contrib import admin

# Register your models here.

from .models import Photo, Back, Coordinated, Image, Post

admin.site.register(Photo)
admin.site.register(Back)
admin.site.register(Coordinated)
admin.site.register(Image)
admin.site.register(Post)
