from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import WatchHistoryViewSet

router = DefaultRouter()
router.register(r'history', WatchHistoryViewSet, basename='watch-history')

urlpatterns = [
    path('', include(router.urls)),
]
