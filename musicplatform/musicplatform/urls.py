from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from albums.views import AlbumViewSet, SongViewSet
from artists.views import ArtistViewSet
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register("artists", ArtistViewSet)
router.register("albums", AlbumViewSet)
router.register("songs", SongViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("auth/",include("users.urls")),
]

# Third-party libraries
urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
