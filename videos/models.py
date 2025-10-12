from django.db import models
from accounts.models import User
# Create your models here.

class Video(models.Model):
    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_videos'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file_url = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=False,
    )
    duration = models.PositiveIntegerField(
        help_text='Duration in seconds'
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    views_count = models.PositiveBigIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title



class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.video.title}'
    
    def __repr__(self):
        return f'{self.user.username} on {self.video.title}'
