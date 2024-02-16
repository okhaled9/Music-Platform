from django_filters import rest_framework as filters
from .models import Album, Song


class AlbumFilter(filters.FilterSet):
    class Meta:
        model = Album
        fields = {
            "name": ["icontains"],
            "cost": ["exact", "lt", "lte", "gt", "gte"],
        }


class SongFilter(filters.FilterSet):
    class Meta:
        model = Song
        fields = {
            "name": ["icontains"],
        }
