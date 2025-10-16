from rest_framework import viewsets, permissions
from videos.models import Video, Comment
from videos.serializers import VideoSerializer, VideoUploadSerializer, CommentSerializer
from .permissions import IsAdminOnly, IsCommentOwnerOrAdmin, CanCommentOnPublicVideo


class VideoViewSet(viewsets.ModelViewSet):
    """
    - Anyone can view public videos
    - Only admins can create, update, or delete videos
    """

    queryset = Video.objects.all().order_by("-upload_date")
    permission_classes = [IsAdminOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return VideoUploadSerializer
        return VideoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin can see all videos
            return Video.objects.all().order_by("-upload_date")
        # Regular users see only public videos
        return Video.objects.filter(is_public=True).order_by("-upload_date")

    def perform_create(self, serializer):
        # Admin uploads videos
        serializer.save(uploader=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    - Authenticated users can comment only on public videos
    - Only the comment owner or admin can update/delete their comment
    """

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsCommentOwnerOrAdmin,
        CanCommentOnPublicVideo,
    ]

    def get_video(self):
        """Helper method required by CanCommentOnPublicVideo"""
        return Video.objects.get(pk=self.kwargs["video_pk"])

    def get_queryset(self):
        return Comment.objects.filter(video_id=self.kwargs["video_pk"]).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, video=self.get_video())
