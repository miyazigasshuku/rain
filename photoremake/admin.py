from django.contrib import admin

# Register your models here.

from .models import User, Photo

admin.site.register(User)
admin.site.register(Photo)