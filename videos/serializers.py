from rest_framework import serializers
from videos.models import Video, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_at"]


class VideoSerializer(serializers.ModelSerializer):
    uploader = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "uploader",
            "title",
            "description",
            "file_url",
            "thumbnail",
            "duration",
            "upload_date",
            "is_public",
            "views_count",
            "likes_count",
            "comments",
        ]


class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "title",
            "description",
            "file_url",
            "thumbnail",
            "duration",
            "is_public",
        ]
