from rest_framework.routers import DefaultRouter

from .views import AuditLogViewSet, LoginHistoryViewSet, ExportLogViewSet, SecurityEventViewSet

router = DefaultRouter()
router.register(r"audit-logs", AuditLogViewSet, basename="audit-logs")
router.register(r"login-history", LoginHistoryViewSet, basename="login-history")
router.register(r"export-logs", ExportLogViewSet, basename="export-logs")
router.register(r"security-events", SecurityEventViewSet, basename="security-events")

urlpatterns = router.urls
