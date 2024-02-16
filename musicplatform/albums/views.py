from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Album, Song
from .serializers import AlbumSerializer, SongSerializer
from .filters import AlbumFilter, SongFilter


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    # filterset_fields = ["cost","name"]
    filterset_class = AlbumFilter

    @action(detail=False, methods=["PATCH"])
    def approve_all(self, request):
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
