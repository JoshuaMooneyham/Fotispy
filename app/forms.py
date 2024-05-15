from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Song


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class AddSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_file', 'title', 'genre', 'artist']

    def clean(self):
        cleaned_data = super().clean()
        songs = Song.objects.filter(title=cleaned_data['title'])
        print(cleaned_data)
        print(songs)
        if len(songs) == 0:
            return cleaned_data
        elif cleaned_data['song_file'].name[-4:] not in ['.mp3', '.ogg']:
            raise forms.ValidationError('Song must be an mp3 or ogg file!')
        else: 
            raise forms.ValidationError('Song already in database!')

# class AddSongForm(forms.Form):
#     song_file = forms.FileField()

#     def clean(self):
#         cleaned_data = super().clean()
#         print('made it here')
#         print(cleaned_data)
#         return cleaned_data