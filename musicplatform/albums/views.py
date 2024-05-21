from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from artists.models import Artist
from .models import Album, Song
from .serializers import AlbumSerializer, SongSerializer
from .filters import AlbumFilter, SongFilter


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    # filterset_fields = ["cost","name"]
    filterset_class = AlbumFilter
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        artist_name = request.data.get("artist")
        user = Artist.objects.get(stage_name = artist_name).user
        if request.user != user:
            return Response({"detail":"You don't have permission to access another artist's resources"},status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        
        instance = self.get_object()

        artist_name=instance.artist
        artist_object=Artist.objects.get(stage_name=artist_name)
        user = artist_object.user

        if  request.user != user:
            return Response({"detail":"You don't have permission to access another artist's resources"},status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("artist"):
            return Response({"detail":"artist cannot be changed"},status=status.HTTP_400_BAD_REQUEST)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        artist_name=instance.artist
        artist_object=Artist.objects.get(stage_name=artist_name)
        user = artist_object.user
        if request.user != user:
            return Response({"detail":"You don't have permission to access another artist's resources"},status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False, methods=["PATCH"])
    def approve_all(self, request):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.is_staff:
            return Response({"detail":"Action forbidden"},status=status.HTTP_403_FORBIDDEN)
        
        try:
            albums = self.get_queryset()
            approve = request.data["approve"]

            if type(request.data["approve"]) != bool:
                raise KeyError("approve is required to be a boolean")

            albums.update(is_approved=approve)
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_400_BAD_REQUEST)

        message = f"all albums {"approved" if approve else "disapproved"}"
        return Response({"message": message}, status=status.HTTP_200_OK)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filterset_class = SongFilter
