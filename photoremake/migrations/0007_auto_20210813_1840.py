# Generated by Django 2.2.24 on 2021-08-13 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoremake', '0006_auto_20210813_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='加工前画像'),
        ),
    ]
