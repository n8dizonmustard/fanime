from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Anime(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    image = models.URLField()
    description = models.TextField(max_length=400)


class Profile(models.Model):
    avatar = models.URLField()
    anime = models.ManyToManyField(Anime)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.CharField(max_length=300)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)