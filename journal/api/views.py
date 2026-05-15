from core.api.mixins import StandardModelViewSet
from core.api.permissions import TeacherOwnSubjectPermission, StudentOwnDataPermission

from journal.models import Schedule, LessonSession, Attendance
from .serializers import ScheduleSerializer, LessonSessionSerializer, AttendanceSerializer


class ScheduleViewSet(StandardModelViewSet):
    queryset = Schedule.objects.filter(is_deleted=False).select_related("organization", "subject_group", "teacher", "auditorium")
    serializer_class = ScheduleSerializer
    permission_classes = [TeacherOwnSubjectPermission]


class LessonSessionViewSet(StandardModelViewSet):
    queryset = LessonSession.objects.filter(is_deleted=False).select_related("schedule", "subject_group", "topic", "teacher")
    serializer_class = LessonSessionSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "subject_group__organization"


class AttendanceViewSet(StandardModelViewSet):
    queryset = Attendance.objects.filter(is_deleted=False).select_related("lesson_session", "student", "student__user", "marked_by")
    serializer_class = AttendanceSerializer
    permission_classes = [StudentOwnDataPermission]
    organization_field = "lesson_session__subject_group__organization"
    student_field = "student"
