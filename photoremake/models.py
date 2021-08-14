from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth import get_user_model


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='images/original/', default='defo')
    uploaded_at = models.DateTimeField(verbose_name='日付',default=now)
    output = models.ImageField( default = 'output/output.jpg')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)