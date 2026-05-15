from rest_framework.routers import DefaultRouter

from .views import OfficialDocumentViewSet, DocumentApprovalViewSet

router = DefaultRouter()
router.register(r"documents", OfficialDocumentViewSet, basename="documents")
router.register(r"document-approvals", DocumentApprovalViewSet, basename="document-approvals")

urlpatterns = router.urls
