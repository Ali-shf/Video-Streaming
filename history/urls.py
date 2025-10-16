from rest_framework.routers import DefaultRouter
from django.urls import path, include
from history.views import WatchHistoryViewSet


router = DefaultRouter()
router.register(r"history", WatchHistoryViewSet, basename="watchhistory")


urlpatterns = [
    path("", include(router.urls)),
]
