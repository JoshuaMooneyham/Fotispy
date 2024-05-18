from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.decorators import *

# Create your views here.
@unauthenticated_user
def AccountCreationView(req: HttpRequest) -> HttpResponse:
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Standard')
            user.groups.add(group)

            messages.success(req, f'Account was created for {form.cleaned_data.get("username")}')

            return redirect('login')

    context = {"form": form}
    return render(req, "register.html", context)

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

def logoutView(req: HttpRequest) -> HttpResponse:
    logout(req)
    return redirect('login')

def home_view(req: HttpRequest) -> HttpResponse:
    songs = Song.objects.all()
    # print(songs[0].song_file.url)
    # context = {'songs': songs}

    return render(req, 'homepage.html')

def add_song_view(req: HttpRequest) -> HttpResponse:
    form = AddSongForm()
    if req.method == 'POST':
        form = AddSongForm(req.POST, req.FILES)
        print(f'Valid: {form.is_valid()}')
        if form.is_valid():
            form.save()
            messages.success(req, 'Song Accepted')

    return render(req, 'add-song.html', {'form': form})

def home_frame(req: HttpRequest) -> HttpResponse:
    songs = Song.objects.all()
    songForm = AddSongForm()
    playlistForm = None
    playlists = None
    if req.user.is_authenticated:
        playlistForm = NewPlaylistForm()
        playlists = req.user.playlist_set.all()

    # if req.method == 'POST':
    #     Playlist.objects.create(name=req.POST.get('name'), description=req.POST.get('description'), created_by=req.user)
    #     form = NewPlaylistForm()
        # print(req.POST)
        # if form.is_valid():
            # form.save()

    if req.method == 'POST':
        if req.POST.get('Add Song'):
            songForm = AddSongForm(req.POST, req.FILES)
            if songForm.is_valid():
                songForm.save()
                messages.success(req, 'Song Accepted')
        # elif req.POST.get('Add Playlist'):


    context = {'songs': songs, 'playlistForm': playlistForm, 'songForm': songForm, 'playlists': playlists}
    return render(req, 'add-song.html', context)