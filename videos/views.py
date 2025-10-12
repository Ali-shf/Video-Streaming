from rest_framework import viewsets, permissions
from .models import Video, Comment
from .serializers import VideoSerializer, VideoUploadSerializer, CommentSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-upload_date')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VideoUploadSerializer
        return VideoSerializer

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(video_id=self.kwargs['video_pk']).order_by('-created_at')

    def perform_create(self, serializer):
        video_id = self.kwargs['video_pk']
        serializer.save(user=self.request.user, video_id=video_id)
