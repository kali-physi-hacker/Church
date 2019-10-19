from django.db import models
from django.contrib.auth.models import User

from Member.models import upload_image_path


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    telephone = models.PositiveIntegerField(blank=True, null=True)
    whatsapp_line = models.PositiveIntegerField(blank=True, null=True)
    facebook_link = models.CharField(max_length=255, blank=True, null=True)
    twitter_link = models.CharField(max_length=255, blank=True, null=True)
    instagram_link = models.CharField(max_length=255, blank=True, null=True)
    picture = models.ImageField(upload_to=upload_image_path, blank=True, null=True)

    def __str__(self):
        return self.user.username

