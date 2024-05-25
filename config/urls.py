"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings  # type: ignore
from django.contrib import admin # type: ignore
from django.urls import path, re_path, URLPattern, URLResolver # type: ignore
from django.views.static import serve # type: ignore
from app.views import *

urlpatterns: list[URLPattern|URLResolver] = [
    path("register/", AccountCreationView),
    path('login/', LogInView, name='login'),
    path('logout/', logoutView, name='logout'),
    path("account/", account_view, name="account"),
    path("account/update/", update_account_view, name="update_account"),
    path("account/update/username/", update_username, name='update_username'),
    path("account/update/email/", update_email, name='update_email'),
    path("account/update/password/", update_password, name='update_password'),
    path('songs/add/', add_song_view, name='add_song'),
    path('songs/delete/<int:songKey>/', delete_song_view, name='delete_song'),
    path('songs/update/<int:songKey>/', update_song_view, name='update_song'),
    path('', home_view, name='home'),
    path("admin/", admin.site.urls),
    path('iframetest/<str:playlistID>/', home_frame, name='ift'),
    path('playlists/delete/<int:playlistId>/', delete_playlist, name='deletePlaylist'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = 'app.views.handle404'