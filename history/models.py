from django.db import models
from accounts.models import User
from videos.models import Video

# Create your models here.


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0) 

    class Meta:
        unique_together = ('user', 'video')  # one record per user-video

    def __str__(self):
        return f"{self.user.username} watched {self.video.title}"
