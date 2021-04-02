from django.db import models

# Create your models here.

class Profile(models.Model):
    # avatar = models.
    # fav_list = models.
    # want_list = models.
    currently_watching_list = models.CharField()

class Anime(models.Model):
    name = models.CharField()
    rating = models.IntegerField()
    # image = models.
    description = models.TextField()