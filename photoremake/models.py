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
    photo = models.ImageField(upload_to='images/original/', verbose_name='加工前画像', blank=True, null=True)
    date = models.DateTimeField(verbose_name='日付',default=now)


class Back(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='背景タイトル', max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)
    back_img = models.ImageField(upload_to='images/back/', verbose_name='背景画像', blank=True, null=True, default="タイトル")

class Coordinated(models.Model):
    id = models.AutoField(primary_key=True)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='加工前画像',  blank=True, null=True)
    back_id = models.ForeignKey(Back, on_delete=models.CASCADE, verbose_name='背景画像',  blank=True, null=True)
    title = models.CharField(verbose_name='タイトル', max_length=50, default="タイトル")
    image = models.ImageField(upload_to='images/coordinated/', verbose_name='加工後画像', blank=True, null=True)
    date = models.DateTimeField(verbose_name='日付',default=now)