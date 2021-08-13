from django.db import models
from datetime import datetime
from django.utils.timezone import now
 
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='名前', max_length=30)
    rank = models.CharField(verbose_name='繰り返しランク', max_length=10)
 
    def __str__(self):
        return self.name
 
 
class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)
    photo = models.ImageField(upload_to='images', verbose_name='加工前画像', blank=True, null=True)
    date = models.DateTimeField(verbose_name='日付',default=now)