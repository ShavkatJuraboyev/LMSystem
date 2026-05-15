from core.api.mixins import StandardModelViewSet
from core.api.permissions import IsAdminOrSuperAdmin

from integrations.models import IntegrationConfig, IntegrationLog, BackupLog, SystemHealthLog
from .serializers import IntegrationConfigSerializer, IntegrationLogSerializer, BackupLogSerializer, SystemHealthLogSerializer


class IntegrationConfigViewSet(StandardModelViewSet):
    queryset = IntegrationConfig.objects.filter(is_deleted=False).select_related("organization")
    serializer_class = IntegrationConfigSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class IntegrationLogViewSet(StandardModelViewSet):
    queryset = IntegrationLog.objects.all().select_related("organization", "integration")
    serializer_class = IntegrationLogSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class BackupLogViewSet(StandardModelViewSet):
    queryset = BackupLog.objects.all().select_related("organization")
    serializer_class = BackupLogSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class SystemHealthLogViewSet(StandardModelViewSet):
    queryset = SystemHealthLog.objects.all()
    serializer_class = SystemHealthLogSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    organization_field = None
