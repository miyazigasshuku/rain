from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth import get_user_model

 
class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)
    photo = models.ImageField(upload_to='images/original/', verbose_name='加工前画像', blank=True, null=True)
    date = models.DateTimeField(verbose_name='日付',default=now)


class Back(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='背景タイトル', max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)
    back_img = models.ImageField(upload_to='images/back/', verbose_name='背景画像', blank=True, null=True, default="タイトル")

class Coordinated(models.Model):
    id = models.AutoField(primary_key=True)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='加工前画像',  blank=True, null=True)
    back_id = models.ForeignKey(Back, on_delete=models.CASCADE, verbose_name='背景画像',  blank=True, null=True)
    title = models.CharField(verbose_name='タイトル', max_length=50, default="タイトル")
    image = models.ImageField(upload_to='images/coordinated/', verbose_name='加工後画像', blank=True, null=True)
    date = models.DateTimeField(verbose_name='日付',default=now)