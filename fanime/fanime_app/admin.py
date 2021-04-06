from django.contrib import admin
from .models import Profile, Comment, Anime, Photo

# Register your models here.
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Anime)
admin.site.register(Photo)