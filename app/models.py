from django.db import models
# from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

# music = FileSystemStorage(location='/media')

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=50)
    song_file = models.FileField(upload_to='')
    artist = models.ManyToManyField(Artist)

    def __str__(self):
        return self.title
    
class Playlist(models.Model):
    name = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



