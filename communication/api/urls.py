from rest_framework.routers import DefaultRouter

from .views import AnnouncementViewSet, DirectMessageViewSet, SupportRequestViewSet

router = DefaultRouter()
router.register(r"announcements", AnnouncementViewSet, basename="announcements")
router.register(r"messages", DirectMessageViewSet, basename="messages")
router.register(r"support-requests", SupportRequestViewSet, basename="support-requests")

urlpatterns = router.urls
