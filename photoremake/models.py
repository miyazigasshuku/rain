from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


class Photo(models.Model):
    title = models.CharField(max_length=30, default='no title')
    photo = models.ImageField(upload_to='images/original/', default='defo',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    output = models.ImageField(default='output/output.jpg')
    author = models.ForeignKey(
        Profile, related_name='photos', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    # def num_likes(self):
    #     return self.liked.all().count()

    class Meta:
        ordering = ('-created',)
