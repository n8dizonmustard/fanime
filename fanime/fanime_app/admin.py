from django.contrib import admin
from .models import Profile, Comment, FavAnime, Photo

# Register your models here.
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(FavAnime)
admin.site.register(Photo)