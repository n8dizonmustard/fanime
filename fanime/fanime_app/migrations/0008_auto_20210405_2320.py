# Generated by Django 3.1.7 on 2021-04-05 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fanime_app', '0007_auto_20210405_2140'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavAnime',
            new_name='FavList',
        ),
        migrations.AddField(
            model_name='profile',
            name='fav_list',
            field=models.ManyToManyField(to='fanime_app.FavList'),
        ),
    ]