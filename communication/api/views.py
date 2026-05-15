from rest_framework.permissions import IsAuthenticated

from core.api.mixins import StandardModelViewSet
from core.api.permissions import ReadOnlyForManagementWriteForAdmin

from communication.models import Announcement, DirectMessage, SupportRequest
from .serializers import AnnouncementSerializer, DirectMessageSerializer, SupportRequestSerializer


class AnnouncementViewSet(StandardModelViewSet):
    queryset = Announcement.objects.filter(is_deleted=False).select_related("organization", "author", "faculty", "department", "group")
    serializer_class = AnnouncementSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class DirectMessageViewSet(StandardModelViewSet):
    queryset = DirectMessage.objects.filter(is_deleted=False).select_related("sender", "receiver")
    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(sender=user) | super().get_queryset().filter(receiver=user)


class SupportRequestViewSet(StandardModelViewSet):
    queryset = SupportRequest.objects.filter(is_deleted=False).select_related("organization", "author", "assigned_to")
    serializer_class = SupportRequestSerializer
    permission_classes = [IsAuthenticated]
