from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group # type: ignore
from django.contrib.auth.decorators import login_required 
from app.forms import *
from app.decorators import *

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
    # if req.method=='GET':
    #     print('hello', req.GET)
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
    context = {'user': req.user if req.user.is_authenticated else None}
    return render(req, 'homepage.html', context)

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

    if req.method == 'POST':
        if req.POST.get('Add Song'):
            songForm = AddSongForm(req.POST, req.FILES)
            if songForm.is_valid():
                songForm.save()
                messages.success(req, 'Song Accepted')
        elif req.POST.get('Add Playlist'):
            Playlist.objects.create(name=req.POST.get('name'), description=req.POST.get('description'), created_by=req.user)
            playlistForm = NewPlaylistForm() if req.user.is_authenticated else None
        elif req.POST.get('Populate Playlist'):
            Playlist.objects.get(pk=req.POST.get('playlistKey')).songs.add(Song.objects.get(pk=req.POST.get('songKey'))) # type: ignore
        elif req.POST.get('Update Playlist'):
            try:
                # updateList = Playlist.objects.get(pk=req.POST.get('playlistKey'))
                playlistInfo.name = req.POST.get('name')
                playlistInfo.description = req.POST.get('description')
                playlistInfo.save()
            except:
                pass
        elif req.POST.get('Remove Song'):
            Playlist.objects.get(pk=req.POST.get('removeSongPlaylistKey')).songs.remove(Song.objects.get(pk=req.POST.get('removeSongKey')))

    context = {'songs': songs, 'playlistForm': playlistForm, 'songForm': songForm, 'playlists': playlists, 'playlistInfo': playlistInfo} # type: ignore
    return render(req, 'add-playlist.html', context) # type: ignore

# ==={ Playlist Deletion }=== #
def delete_playlist(req: HttpRequest, playlistId: int) -> HttpResponseRedirect|HttpResponsePermanentRedirect:
    try:
        Playlist.objects.get(pk=f'{playlistId}').delete()
    except:
        messages.error(req, 'Playlist could not be found')
    return redirect('/iframetest/none')

# ==={ View Account }=== #
@login_required(login_url='login')
def account_view(req: HttpRequest) -> HttpResponse: 
    userRoles = [i.name for i in req.user.groups.all()] # type: ignore
    songs = Song.objects.all() if 'Admin' in userRoles else None
    playlists = req.user.playlist_set.all() # type: ignore
    return render(req, 'account-view.html', {'user': req.user, 'roles': userRoles, 'songs': songs, 'playlists': playlists})

# ==={ Add Songs }=== #
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

# ==={ Delete Songs }=== #
@allowed_users(allowed_roles=['Admin'])
def delete_song_view(req:HttpRequest, songKey:int) -> HttpResponse:
    try:
        Song.objects.get(pk=f'{songKey}').delete()
    except:
        print('failed altogether')
    return redirect('home')
    # return HttpResponse('waiting')

# ==={ Update Songs }=== #
@allowed_users(allowed_roles=['Admin'])
def update_song_view(req: HttpRequest, songKey: int) -> HttpResponse|HttpResponsePermanentRedirect:
    song = None
    try:
        song = Song.objects.get(pk=f'{songKey}')
    except:
        messages.error(req, 'Song could not be found')
        return redirect('account')
    form = UpdateSongForm()
    # print(req.POST)
    if req.method == 'POST':
        form = UpdateSongForm(req.POST)
        if form.is_valid():
            song.title = form.cleaned_data['title']
            song.genre.clear()
            for genre in form.cleaned_data['genre']:
                song.genre.add(genre)
            song.artist.clear()
            for artist in form.cleaned_data['artist']:
                song.artist.add(artist)
            song.save()
            return redirect('account')

        else:
            print('invalid')
    
    # if req.method == 'POST':
    #     artist = req.POST.get('Artist')
    #     title = req.POST.get('Title')
    #     genre = req.POST.get('Genre1')
    #     genre2 = req.POST.get('Genre2')
    # else:
    #     pass

    return render(req, 'update-song.html', {'song': song, 'form': form})

## ==={ Update Account }=== #
# @login_required
# def update_account_view(req):
#     form = UserCreationForm()
#     return render(req, 'update_account.html', {'form': form})