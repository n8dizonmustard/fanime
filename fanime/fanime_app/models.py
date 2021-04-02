from django.db import models

# Create your models here.

class Profile(models.Model):
     avatar = models.URLField()
     #fav_list = models.
     #want_list = models.
     #currently_watching_list = models.CharField()

class Anime(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    image = models.URLField()
    description = models.TextField(max_length=400)