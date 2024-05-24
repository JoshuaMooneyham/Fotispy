from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User # type: ignore
from app.models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class AddSongFileForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_file']

    # def clean(self):
    #     print(self.cleaned_data)
    #     cleaned_data = super().clean()

    #     if self.data.get('genreInput'):
    #         name = self.data.get('genreInput')
    #         try:
    #             genre = Genre.objects.get(name=f'{name}'.title())
    #         except:
    #             genre = Genre.objects.create(name=f'{name}'.title())
            
    #         cleaned_data['genre'] = Genre.objects.filter(pk=genre.pk)
        
    #     if self.data.get('artistInput'):
    #         try:
    #             artist = Artist.objects.get(name=self.data.get('artistInput'))
    #         except:
    #             artist = Artist.objects.create(name=self.data.get('artistInput'))
    #         cleaned_data['artist'] = Artist.objects.filter(pk=artist.pk)

    #     # if cleaned_data['song_file'].name[-4:] not in ['.mp3', '.ogg']:
    #     #     raise forms.ValidationError('Song must be an mp3 or ogg file!')
        
    #     songs = Song.objects.filter(title=cleaned_data['title'])
    #     print(f'cleaned: {cleaned_data}')

    #     if len(songs) == 0:
    #         return cleaned_data
    #     else:
    #         for song in songs:
    #             for artist in cleaned_data['artist']:
    #                 if artist in song.artist.all():
    #                     raise forms.ValidationError("There is already a song with this Author and Title")
    #         else:
    #             return cleaned_data

class AddSongForm(forms.Form):
    song_file = forms.FileField(required=True)
    genre = forms.CharField(max_length=50, required=True)
    genre2 = forms.CharField(required=False, max_length=50)
    artist = forms.CharField(max_length=50, required=True)
    title = forms.CharField(max_length=50, required=True)

class NewPlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description']

class UpdateSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'genre', 'artist']        