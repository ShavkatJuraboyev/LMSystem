from rest_framework.routers import DefaultRouter

from .views import AssessmentTypeViewSet, GradeViewSet, GradeHistoryViewSet, AppealViewSet

router = DefaultRouter()
router.register(r"assessment-types", AssessmentTypeViewSet, basename="assessment-types")
router.register(r"grades", GradeViewSet, basename="grades")
router.register(r"grade-history", GradeHistoryViewSet, basename="grade-history")
router.register(r"appeals", AppealViewSet, basename="appeals")

urlpatterns = router.urls
