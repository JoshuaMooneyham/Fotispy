from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group # type: ignore
from django.contrib.auth.decorators import login_required 
from app.forms import *
from app.decorators import *
import pathlib
import os

# Create your views here.

# ==={ Create Account }===
@unauthenticated_user
def AccountCreationView(req: HttpRequest) -> HttpResponse:
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='Standard')
            user.groups.add(group)

            messages.success(req, f'Account was created for {form.cleaned_data.get("username")}')

            return redirect('login')

    context = {"form": form}
    return render(req, "register.html", context)

# ==={ Log In }===
@unauthenticated_user
def LogInView(req: HttpRequest) -> HttpResponse:
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.info(req, 'Username or Password incorrect')

    return render(req, 'login.html')

# ==={ Log Out }===
def logoutView(req: HttpRequest) -> HttpResponse:
    logout(req)
    return redirect('login')

# ==={ Media Player }===
def home_view(req: HttpRequest) -> HttpResponse:
    return render(req, 'homepage.html')

# ==={ Homepage }===
def home_frame(req: HttpRequest, playlistID:str) -> HttpResponse:
    songs = Song.objects.all()
    songForm = AddSongForm()
    playlistForm = None
    playlists = None
    if req.user.is_authenticated:
        playlistForm = NewPlaylistForm()
        playlists = req.user.playlist_set.all() # type: ignore
    try:
        playlistInfo = Playlist.objects.get(pk=playlistID)
    except:
        playlistInfo = None

    print(req.POST)
    if req.method == 'POST':
        if req.POST.get('Add Song'):
            songForm = AddSongForm(req.POST, req.FILES)
            if songForm.is_valid():
                songForm.save()
                messages.success(req, 'Song Accepted')
        if req.POST.get('Add Playlist'):
            Playlist.objects.create(name=req.POST.get('name'), description=req.POST.get('description'), created_by=req.user)
            playlistForm = NewPlaylistForm() if req.user.is_authenticated else None
        if req.POST.get('Populate Playlist'):
            Playlist.objects.get(pk=req.POST.get('playlistKey')).songs.add(Song.objects.get(pk=req.POST.get('songKey'))) # type: ignore
            print('hi')
        if req.POST.get('Update Playlist'):
            try:
                # updateList = Playlist.objects.get(pk=req.POST.get('playlistKey'))
                playlistInfo.name = req.POST.get('name')
                playlistInfo.description = req.POST.get('description')
                playlistInfo.save()
            except:
                pass


    print(req.POST)
    context = {'songs': songs, 'playlistForm': playlistForm, 'songForm': songForm, 'playlists': playlists, 'playlistInfo': playlistInfo} # type: ignore
    return render(req, 'add-playlist.html', context) # type: ignore

# ==={ Playlist Deletion }===
def delete_playlist(req: HttpRequest, playlistId: int) -> HttpResponseRedirect|HttpResponsePermanentRedirect:
    try:
        Playlist.objects.get(pk=f'{playlistId}').delete()
    except:
        messages.error(req, 'Playlist could not be found')
    return redirect('/iframetest/none')

# ==={ View Account }===
@login_required(login_url='login')
def account_view(req): 
    return render(req, 'account-view.html', {'user': req.user})

# ==={ Add Songs }===
@allowed_users(allowed_roles=['Admin'])
def add_song_view(req: HttpRequest) -> HttpResponse:
    form = AddSongForm()
    if req.method == 'POST':
        form = AddSongForm(req.POST, req.FILES)
        print(f'Valid: {form.is_valid()}')
        if form.is_valid():
            form.save()
            messages.success(req, 'Song Accepted')
    return render(req, 'add-song.html', {'form': form})

# ==={ Delete Songs }===
@allowed_users(allowed_roles=['Admin'])
def delete_song_view(req, songKey):
    try:
        song = Song.objects.get(pk=f'{songKey}')
        print(song.song_file)
        pathlib.Path(f'{song.song_file.url}').unlink()
        print('IT WAS FOUND')
        # song.delete()
    except:
        print('failed altogether')
    # return redirect('home')
    return HttpResponse('waiting')