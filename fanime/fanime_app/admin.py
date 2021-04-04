from django.contrib import admin
from .models import Anime, Profile, Comment

# Register your models here.
admin.site.register(Anime)
admin.site.register(Profile)
admin.site.register(Comment)