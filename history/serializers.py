from rest_framework import serializers
from history.models import WatchHistory
from videos.models import Video


class WatchHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'video', 'watched_at', 'progress']
