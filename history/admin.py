from django.contrib import admin
from history.models import WatchHistory

# Register your models here.


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ("watched_at",)
    search_fields = ("user__username", "video__title")
