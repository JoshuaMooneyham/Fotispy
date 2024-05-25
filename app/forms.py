import re
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

class AddSongForm(forms.Form):
    song_file = forms.FileField(required=True)
    genre = forms.CharField(max_length=25, required=True)
    genre2 = forms.CharField(required=False, max_length=25)
    artist = forms.CharField(max_length=50, required=True)
    title = forms.CharField(max_length=50, required=True)

class UpdateSongForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    artist = forms.CharField(max_length=50, required=True)
    genre = forms.CharField(max_length=25, required=True)
    genre2 = forms.CharField(max_length=25, required=False)

class NewPlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description']

class UpdatePassword(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']

class UpdateEmail(forms.Form):
    email = forms.EmailField(required=True)

class UpdateUsername(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    help_texts = ['- Must be within 1-150 characters', '- Must only contain alphanumeric characters (including +-.@_)']

    def clean(self):
        cleaned_data = super().clean()
        regexTest = re.findall(r'[\w\+\.\@\-]', cleaned_data.get('username'))
        if len(regexTest) == len(cleaned_data['username']):
            if len(User.objects.filter(username=cleaned_data['username'])) == 0:
                return cleaned_data
            else:
                raise forms.ValidationError('A user with that username already exists')
        else:
            raise forms.ValidationError('Illegal character entered')
        