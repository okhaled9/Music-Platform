from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Artist
from .serializers import ArtistSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "No authentication provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user"] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "No authentication provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        instance = self.get_object()

        user = instance.user
        if request.user != user:
            return Response(
                {
                    "detail": "You do not have permission to access another user's resources"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "No authentication provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        user = instance.user
        if request.user != user:
            return Response(
                {
                    "detail": "You do not have permission to access another user's resources"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
