from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friend_owner', on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friend_list')

    def __str__(self):
        return f"{self.user.username}'s friends"

class SavedProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_user = models.ForeignKey(User, related_name='saved_profiles', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.saved_user.username}'s profile"


# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    updated = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)