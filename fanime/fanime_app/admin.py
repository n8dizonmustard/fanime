from django.contrib import admin
from .models import Profile, Comment, FavList, Photo

# Register your models here.
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(FavList)
admin.site.register(Photo)