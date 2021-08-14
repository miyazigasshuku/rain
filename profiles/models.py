from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models import Q
import uuid


class ProfileManager(models.Manager):
    def get_all_profiles_without_me(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="よろしくお願いします。", max_length=300)
    avatar = models.ImageField(
        default='avatar.png', upload_to='images/avatar/')
    # friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profiles:profile-detail', kwargs={'slug': self.slug})

    def get_posts_count(self):
        return self.photos.all().count()

    def get_all_authors_posts(self):
        return self.photos.all()

    def save(self, *args, **kwargs):
        self.slug = str(uuid.uuid4())[:6]
        ex = Profile.objects.filter(slug=self.slug).exists()
        while ex:
            self.slug = str(uuid.uuid4())[:6]
            ex = Profile.objects.filter(slug=self.slug).exists()
        return super().save(*args, **kwargs)
