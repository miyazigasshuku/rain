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
    # uploaded_at = models.DateTimeField(verbose_name='日付', default=now)
    output = models.ImageField(default='output/output.jpg')
    # user = models.ForeignKey(get_user_model(
    # ), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)
    author = models.ForeignKey(
        Profile, related_name='photos', on_delete=models.CASCADE)
    # liked = models.ManyToManyField(
    #     Profile, blank=True, related_name='likes')  # いいねは、他人のプロフィール
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    # def num_likes(self):
    #     return self.liked.all().count()

    class Meta:
        ordering = ('-created',)
