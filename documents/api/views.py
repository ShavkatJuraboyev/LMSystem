from core.api.mixins import StandardModelViewSet
from core.api.permissions import DocumentWorkflowPermission

from documents.models import OfficialDocument, DocumentApproval
from .serializers import OfficialDocumentSerializer, DocumentApprovalSerializer


class OfficialDocumentViewSet(StandardModelViewSet):
    queryset = OfficialDocument.objects.filter(is_deleted=False).select_related("organization", "author", "signed_by")
    serializer_class = OfficialDocumentSerializer
    permission_classes = [DocumentWorkflowPermission]


class DocumentApprovalViewSet(StandardModelViewSet):
    queryset = DocumentApproval.objects.filter(is_deleted=False).select_related("document", "approver")
    serializer_class = DocumentApprovalSerializer
    permission_classes = [DocumentWorkflowPermission]
    organization_field = "document__organization"
