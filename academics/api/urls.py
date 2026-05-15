from rest_framework.routers import DefaultRouter

from .views import CurriculumViewSet, SubjectViewSet, CurriculumSubjectViewSet, SubjectGroupViewSet, TopicViewSet, LearningContentViewSet, ContentViewViewSet

router = DefaultRouter()
router.register(r"curriculums", CurriculumViewSet, basename="curriculums")
router.register(r"subjects", SubjectViewSet, basename="subjects")
router.register(r"curriculum-subjects", CurriculumSubjectViewSet, basename="curriculum-subjects")
router.register(r"subject-groups", SubjectGroupViewSet, basename="subject-groups")
router.register(r"topics", TopicViewSet, basename="topics")
router.register(r"contents", LearningContentViewSet, basename="contents")
router.register(r"content-views", ContentViewViewSet, basename="content-views")

urlpatterns = router.urls
