from .models import Artist
from .serializers import ArtistSerializer
from rest_framework import viewsets


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer