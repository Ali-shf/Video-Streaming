from django.contrib import admin
from videos.models import Video, Comment

# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "duration",
        "is_public",
        "views_count",
        "likes_count",
    )
    search_fields = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at")
    search_fields = ("text", "user__username")
