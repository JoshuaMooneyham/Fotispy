from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=50)
    song_file = models.FileField(upload_to='')
    artist = models.ManyToManyField(Artist) # type: ignore
    genre = models.ManyToManyField(Genre) # type: ignore

    def __str__(self):
        return self.title
    
class Playlist(models.Model):
    name = models.CharField(max_length=30)
    songs = models.ManyToManyField(Song) # type: ignore
    description = models.CharField(max_length=150, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name