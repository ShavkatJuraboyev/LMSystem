from rest_framework.routers import DefaultRouter

from .views import ScheduleViewSet, LessonSessionViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r"schedules", ScheduleViewSet, basename="schedules")
router.register(r"lesson-sessions", LessonSessionViewSet, basename="lesson-sessions")
router.register(r"attendances", AttendanceViewSet, basename="attendances")

urlpatterns = router.urls
