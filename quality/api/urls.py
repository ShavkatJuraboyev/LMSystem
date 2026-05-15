from rest_framework.routers import DefaultRouter

from .views import QualityInspectionViewSet, DeficiencyViewSet, SurveyViewSet, SurveyQuestionViewSet, SurveyResponseViewSet

router = DefaultRouter()
router.register(r"inspections", QualityInspectionViewSet, basename="inspections")
router.register(r"deficiencies", DeficiencyViewSet, basename="deficiencies")
router.register(r"surveys", SurveyViewSet, basename="surveys")
router.register(r"survey-questions", SurveyQuestionViewSet, basename="survey-questions")
router.register(r"survey-responses", SurveyResponseViewSet, basename="survey-responses")

urlpatterns = router.urls
