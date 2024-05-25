from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.models import Group # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import update_session_auth_hash #type:ignore
from app.forms import *
from app.decorators import *

# Create your views here.

# ==={ Redirect on 404 }===
def handle404(req, *a, **k): #type:ignore
    return redirect('home')

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
        if req.POST.get('Add Playlist'):
            Playlist.objects.create(name=req.POST.get('name'), description=req.POST.get('description'), created_by=req.user)
            playlistForm = NewPlaylistForm() if req.user.is_authenticated else None

        elif req.POST.get('Populate Playlist'):
            Playlist.objects.get(pk=req.POST.get('playlistKey')).songs.add(Song.objects.get(pk=req.POST.get('songKey'))) # type: ignore

        elif req.POST.get('Update Playlist'):
            try:
                playlistInfo.name = req.POST.get('name') #type:ignore
                playlistInfo.description = req.POST.get('description') #type:ignore
                playlistInfo.save() #type:ignore
            except:
                pass

        elif req.POST.get('Remove Song'):
            Playlist.objects.get(pk=req.POST.get('removeSongPlaylistKey')).songs.remove(Song.objects.get(pk=req.POST.get('removeSongKey'))) #type:ignore

    context = {'songs': songs, 'playlistForm': playlistForm, 'songForm': songForm, 'playlists': playlists, 'playlistInfo': playlistInfo} # type: ignore
    return render(req, 'add-playlist.html', context) # type: ignore

# ==={ Playlist Deletion }=== #
def delete_playlist(req: HttpRequest, playlistId: int) -> HttpResponseRedirect|HttpResponsePermanentRedirect:
    try:
        Playlist.objects.get(pk=f'{playlistId}').delete()
    except:
        pass
    return redirect('/iframetest/none/')

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
        print(req.POST)
        print(f'Valid: {form.is_valid()}')

        if form.is_valid():
            try:
                genre = [Genre.objects.get(name=f'{form.cleaned_data["genre"]}'.title())]
            except:
                genre = [Genre.objects.create(name=f'{form.cleaned_data["genre"]}'.title())]

            if form.cleaned_data.get('genre2'):
                try:
                    genre += [Genre.objects.get(name=f'{form.cleaned_data["genre2"]}'.title())]
                except:
                    genre += [Genre.objects.create(name=f'{form.cleaned_data["genre2"]}'.title())]

            try:
                artist = Artist.objects.get(name=form.cleaned_data['artist'])
            except:
                artist = Artist.objects.create(name=form.cleaned_data['artist'])

            try:
                song = Song.objects.create(song_file=form.cleaned_data['song_file'], title=f"{form.cleaned_data['title']}".title())
                song.artist.add(artist) #type:ignore

                for g in genre:
                    if g not in song.genre.all(): #type:ignore
                        song.genre.add(g) #type:ignore
                return redirect('account')
            
            except:
                print('Something Broke')
                form = AddSongForm()
            
    return render(req, 'add-song.html', {'form': form, 'genres': Genre.objects.all()})

# ==={ Delete Songs }=== #
@allowed_users(allowed_roles=['Admin'])
def delete_song_view(req:HttpRequest, songKey:int) -> HttpResponse:
    try:
        Song.objects.get(pk=f'{songKey}').delete()
    except:
        print('failed altogether')
    return redirect('account')

# ==={ Update Songs }=== #
@allowed_users(allowed_roles=['Admin'])
def update_song_view(req: HttpRequest, songKey: int) -> HttpResponse|HttpResponsePermanentRedirect:
    song = None
    try:
        song = Song.objects.get(pk=f'{songKey}')
    except:
        return redirect('account')
    form = UpdateSongForm()
    print(req.POST)

    if req.method == 'POST':
        form = UpdateSongForm(req.POST)
        if form.is_valid():
            print("VALID WOO")
            try:
                genre = [Genre.objects.get(name=f'{form.cleaned_data["genre"]}'.title())]
            except:
                genre = [Genre.objects.create(name=f'{form.cleaned_data["genre"]}'.title())]

            if form.cleaned_data.get('genre2'):
                try:
                    genre += [Genre.objects.get(name=f'{form.cleaned_data["genre2"]}'.title())]
                except:
                    genre += [Genre.objects.create(name=f'{form.cleaned_data["genre2"]}'.title())]

            try:
                artist = Artist.objects.get(name=form.cleaned_data['artist'])
            except:
                artist = Artist.objects.create(name=form.cleaned_data['artist'])

            try: 
                song.genre.clear()  #type:ignore
                song.artist.clear() #type:ignore
                song.title = f'{form.cleaned_data["title"]}'.title()

                for gen in genre:
                    if gen not in song.genre.all(): #type:ignore
                        song.genre.add(gen) #type:ignore
            
                song.artist.add(artist) #type:ignore
                song.save()
                return redirect('account')
            
            except:
                form = UpdateSongForm()
                print('something didnt work')

        else:
            print('invalid')

    return render(req, 'update-song.html', {'song': song, 'form': form})

# ==={ Update Account Base }===
@login_required(login_url='login')
def update_account_view(req: HttpRequest):
    
    return render(req, 'update_account.html')

@login_required(login_url='login')
def update_password(req: HttpRequest):
    form = UpdatePassword()
    errors = None
    if req.method == "POST":
        form = UpdatePassword(req.POST)
        if form.is_valid():
            user = req.user
            req.user.set_password(form.cleaned_data.get('password1'))
            req.user.save()
            update_session_auth_hash(req, user)
            return redirect('update_account')
        else:
            errors = form.errors['password2']
    return render(req, 'update_password.html', {'form': form, 'errors': errors})

@login_required(login_url='login')
def update_email(req: HttpRequest):
    form = UpdateEmail()
    errors = None
    if req.method == "POST":
        form = UpdateEmail(req.POST)
        if form.is_valid():
            req.user.email = form.cleaned_data.get('email')
            req.user.save()
            return redirect('update_account')
        else:
            errors = form.errors['email']
    
    return render(req, 'update_email.html', {'form': form, 'errors': errors})

@login_required(login_url='login')
def update_username(req: HttpRequest):
    form = UpdateUsername()
    errors = None

    if req.method == "POST":
        form = UpdateUsername(req.POST)
        if form.is_valid():
            req.user.username = form.cleaned_data.get('username')
            req.user.save()
            return redirect('update_account')
        else:
            errors = form.errors['__all__']
    
    return render(req, 'update_username.html', {'form': form, 'errors': errors})