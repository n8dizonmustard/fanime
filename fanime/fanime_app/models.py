from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    # avatar = models.
    # fav_list = models.
    # want_list = models.
    currently_watching_list = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Anime(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    # image = models.
    description = models.TextField()