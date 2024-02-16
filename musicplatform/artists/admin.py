from django.contrib import admin
from .models import Artist
from albums.models import Album


class AlbumInline(admin.TabularInline):
    model = Album
    extra = 0
    readonly_fields = ["creation_datetime"]


class ArtistAdmin(admin.ModelAdmin):
    list_display = ["stage_name", "get_approved"]
    inlines = [AlbumInline]

    @admin.display(description="APPROVED ALBUMS")
    def get_approved(self, obj):
        return obj.approved_albums

    get_approved.admin_order_field = "approved_albums"


admin.site.register(Artist, ArtistAdmin)
