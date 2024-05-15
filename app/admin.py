from django.contrib import admin
from app.models import *

# Register your models here.

admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Artist)
admin.site.register(Genre)