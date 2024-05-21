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
    filterset_class = AlbumFilter
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            artist = Artist.objects.get(user=request.user)
        except Exception:
            return Response({"detail":"This user is not an artist"},status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["artist"] = artist

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        
        instance = self.get_object()

        user=instance.artist.user
        if  request.user != user:
            return Response({"detail":"You do not have permission to access another user's resources"},status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        user = instance.artist.user
        if request.user != user:
            return Response({"detail":"You do not have permission to access another user's resources"},status=status.HTTP_403_FORBIDDEN)

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

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            Artist.objects.get(user=request.user)
        except Exception:
            return Response({"detail":"This user is not an artist"},status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        album_id = request.data.get("album")        
        album_obj = Album.objects.get(id=album_id)
        user = album_obj.artist.user
        
        if request.user != user:
            return Response({"detail":"You do not have permission to access another user's resources"},status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()

        user = instance.album.artist.user
        if request.user != user:
            return Response({"detail":"You do not have permission to access another user's resources"},status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail":"No authentication provided"},status=status.HTTP_401_UNAUTHORIZED)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        user = instance.album.artist.user
        if request.user != user:
            return Response({"detail":"You do not have permission to access another user's resources"},status=status.HTTP_403_FORBIDDEN)
        
        target_album_id = request.data.get("album")
        try:
            target_album_obj = Album.objects.get(id=target_album_id)
        except Exception:
            return Response({"detail":"album not found"}, status=status.HTTP_404_NOT_FOUND)
        
        target_album_user = target_album_obj.artist.user
        if request.user != target_album_user:
            return Response({"detail":"cannot allocate song to another user's album"},status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
