from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth import get_user_model
import PIL.Image
from numpy.lib.npyio import save
from .utils import get_filtered_image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='images/original/', default='defo')
    uploaded_at = models.DateTimeField(verbose_name='日付',default=now)
    output = models.ImageField( default = 'output/output.jpg')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)

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
    uploaded_at = models.DateTimeField(verbose_name='日付',default=now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー',  blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        pil_img = PIL.Image.open(self.image)
        cv_img = np.array(pil_img)
        print("----cv_img-------")
        print(cv_img)
        img = get_filtered_image(cv_img, self.action)
        print("-------img-------")
        print(img)
        im_pil = PIL.Image.fromarray(img)
        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()
        self.image.save(str(self.image), ContentFile(image_png), save=False)
        super().save(*args, **kwargs)