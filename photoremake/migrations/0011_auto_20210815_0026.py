# Generated by Django 2.2.24 on 2021-08-14 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoremake', '0010_auto_20210814_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(default='defo', upload_to='images/original/'),
        ),
    ]