from django.db import models
from users.models import User


class Artist(models.Model):
    stage_name = models.CharField(primary_key=True, max_length=50)
    social_link = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def approved_albums(self):
        return self.album_set.filter(is_approved=True).count()

    def __str__(self):
        return self.stage_name

    class Meta:
        ordering = ["stage_name"]
