from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

#Im thinking instead of saving all the anime info we save the anime id or the anime link
#for example cowboy bebop id is 1 and the link is https://kitsu.io/api/edge/anime/1 
#I think we can work with that
class Anime(models.Model):
    api_link = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.CharField(max_length=300)
    anime_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)