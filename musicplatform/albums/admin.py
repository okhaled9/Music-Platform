from django.contrib import admin
from django import forms
from .models import Album, Song


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        help_texts = {"is_approved": "Approve the album if its name is not explicit"}
        exclude = []


class AlbumAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "creation_datetime"]
    form = AlbumForm


admin.site.register(Album, AlbumAdmin)
admin.site.register(Song)
