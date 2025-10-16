# videos/permissions.py
from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """Allow only admins (staff users) to create, edit, or delete videos."""

    def has_permission(self, request, view):
        # Safe methods (GET, HEAD, OPTIONS) allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # For POST, PUT, PATCH, DELETE → only admins
        return request.user and request.user.is_staff


class IsCommentOwnerOrAdmin(permissions.BasePermission):
    """Allow only the comment owner or admin to delete/update comment."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff


class CanCommentOnPublicVideo(permissions.BasePermission):
    """Allow commenting only on public videos."""

    def has_permission(self, request, view):
        if view.action == "create":
            video = view.get_video()  # helper defined in the viewset
            return video.is_public
        return True
