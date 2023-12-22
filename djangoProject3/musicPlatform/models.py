from django.db import models
from django.contrib.auth.models import User
import librosa


# Create your models here.

class Music(models.Model):
    title = models.CharField(max_length=256)
    artist = models.CharField(max_length=256, null=True)
    url = models.CharField(max_length=256, null=True)
    loi = models.TextField(null=True)
    image = models.ImageField(upload_to="images", null=True)
    create_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now=True)
    music = models.ForeignKey(Music, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images/review", null=True)


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user.username}: {self.message}'
