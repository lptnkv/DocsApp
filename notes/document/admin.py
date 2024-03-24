from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Document, NotesUser

admin.site.register([Document, NotesUser])