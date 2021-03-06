from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User




class Anime(models.Model):
    api_id = models.CharField(max_length=10)
    api_name = models.CharField(max_length=100)
    api_img = models.CharField(max_length=100)
    def __str__(self):
        return self.api_name


class Profile(models.Model):
    name = models.CharField(max_length=100)
    favorite_anime_ever = models.CharField(max_length=100)
    about = models.TextField(max_length=250)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favs = models.ManyToManyField(Anime)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile')

class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.profile_id} @{self.url}"
        
class Comment(models.Model):
    comment = models.CharField(max_length=300)
    anime_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.comment}"