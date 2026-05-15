from core.api.mixins import StandardModelViewSet
from core.api.permissions import IsManagementRole

from analytics.models import KPISnapshot, RiskAlert
from .serializers import KPISnapshotSerializer, RiskAlertSerializer


class KPISnapshotViewSet(StandardModelViewSet):
    queryset = KPISnapshot.objects.filter(is_deleted=False).select_related("organization")
    serializer_class = KPISnapshotSerializer
    permission_classes = [IsManagementRole]


class RiskAlertViewSet(StandardModelViewSet):
    queryset = RiskAlert.objects.filter(is_deleted=False).select_related("organization", "user", "student", "subject_group", "resolved_by")
    serializer_class = RiskAlertSerializer
    permission_classes = [IsManagementRole]
