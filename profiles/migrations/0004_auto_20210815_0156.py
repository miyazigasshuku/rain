# Generated by Django 2.2.24 on 2021-08-14 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar.png', upload_to='images/avatar/'),
        ),
    ]