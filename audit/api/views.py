from core.api.mixins import StandardModelViewSet
from core.api.permissions import IsAdminOrSuperAdmin, IsManagementRole

from audit.models import AuditLog, LoginHistory, ExportLog, SecurityEvent
from .serializers import AuditLogSerializer, LoginHistorySerializer, ExportLogSerializer, SecurityEventSerializer


class AuditLogViewSet(StandardModelViewSet):
    queryset = AuditLog.objects.all().select_related("user", "organization")
    serializer_class = AuditLogSerializer
    permission_classes = [IsManagementRole]

    def perform_create(self, serializer):
        raise PermissionError("Audit log API orqali yaratilmaydi.")


class LoginHistoryViewSet(StandardModelViewSet):
    queryset = LoginHistory.objects.all().select_related("user", "organization")
    serializer_class = LoginHistorySerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def perform_create(self, serializer):
        raise PermissionError("Login tarixi API orqali yaratilmaydi.")


class ExportLogViewSet(StandardModelViewSet):
    queryset = ExportLog.objects.all().select_related("user", "organization")
    serializer_class = ExportLogSerializer
    permission_classes = [IsManagementRole]


class SecurityEventViewSet(StandardModelViewSet):
    queryset = SecurityEvent.objects.all().select_related("organization", "user", "resolved_by")
    serializer_class = SecurityEventSerializer
    permission_classes = [IsAdminOrSuperAdmin]
