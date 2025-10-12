from rest_framework import serializers
from .models import WatchHistory


class WatchHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    video = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'video', 'watched_at', 'progress']
