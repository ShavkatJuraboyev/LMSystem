from rest_framework.routers import DefaultRouter

from .views import KPISnapshotViewSet, RiskAlertViewSet

router = DefaultRouter()
router.register(r"kpi", KPISnapshotViewSet, basename="kpi")
router.register(r"risk-alerts", RiskAlertViewSet, basename="risk-alerts")

urlpatterns = router.urls
