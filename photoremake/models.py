from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth import get_user_model
# from PIL import Image
import PIL.Image
from numpy.lib.npyio import save
from .utils import get_filtered_image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(
    ), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)
    photo = models.ImageField(
        upload_to='images/original/', verbose_name='加工前画像', blank=True, null=True)
    date = models.DateTimeField(verbose_name='日付', default=now)

    def __str__(self):
        return str(self.id)


class Back(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='背景タイトル', max_length=50)
    user = models.ForeignKey(get_user_model(
    ), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)
    back_img = models.ImageField(
        upload_to='images/back/', verbose_name='背景画像', blank=True, null=True, default="タイトル")


class Coordinated(models.Model):
    id = models.AutoField(primary_key=True)
    photo_id = models.ForeignKey(
        Photo, on_delete=models.CASCADE, verbose_name='加工前画像',  blank=True, null=True)
    back_id = models.ForeignKey(
        Back, on_delete=models.CASCADE, verbose_name='背景画像',  blank=True, null=True)
    title = models.CharField(
        verbose_name='タイトル', max_length=50, default="タイトル")
    image = models.ImageField(
        upload_to='images/coordinated/', verbose_name='加工後画像', blank=True, null=True)
    date = models.DateTimeField(verbose_name='日付', default=now)


ACTION_CHOICES = (
    ('NO_FILTER', 'no filter'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', 'blurred'),
    ('BINARY', 'binary'),
    ('INVERT', 'invert')
)


class Image(models.Model):
    title = models.CharField(max_length=20, default='no title')
    image = models.ImageField(upload_to='images/photo/', blank=True, null=True)
    action = models.CharField(
        max_length=30, choices=ACTION_CHOICES, default='NO_FILTER')
    # photo = models.ImageField(upload_to='images/photo/', default='default')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # output = models.ImageField(default='output/output.jpg')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        pil_img = PIL.Image.open(self.image)
        cv_img = np.array(pil_img)
        img = get_filtered_image(cv_img, self.action)
        im_pil = PIL.Image.fromarray(img)
        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()
        self.image.save(str(self.image), ContentFile(image_png), save=False)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=20, default='no title')
    file = models.ImageField(upload_to='images/file/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
