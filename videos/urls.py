from rest_framework.routers import DefaultRouter
from django.urls import path, include
from videos.views import VideoViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"videos", VideoViewSet, basename="video")

# Nested route for comments
comment_list = CommentViewSet.as_view({"get": "list", "post": "create"})

urlpatterns = [
    path("", include(router.urls)),
    path("videos/<int:video_pk>/comments/", comment_list, name="video-comments"),
]
