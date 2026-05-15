from rest_framework.routers import DefaultRouter

from .views import IntegrationConfigViewSet, IntegrationLogViewSet, BackupLogViewSet, SystemHealthLogViewSet

router = DefaultRouter()
router.register(r"configs", IntegrationConfigViewSet, basename="configs")
router.register(r"logs", IntegrationLogViewSet, basename="logs")
router.register(r"backups", BackupLogViewSet, basename="backups")
router.register(r"health", SystemHealthLogViewSet, basename="health")

urlpatterns = router.urls
