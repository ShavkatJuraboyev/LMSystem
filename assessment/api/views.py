from core.api.mixins import StandardModelViewSet
from core.api.permissions import ReadOnlyForManagementWriteForAdmin, StudentOwnDataPermission, TeacherOwnSubjectPermission

from assessment.models import AssessmentType, Grade, GradeHistory, Appeal
from .serializers import AssessmentTypeSerializer, GradeSerializer, GradeHistorySerializer, AppealSerializer


class AssessmentTypeViewSet(StandardModelViewSet):
    queryset = AssessmentType.objects.filter(is_deleted=False).select_related("organization")
    serializer_class = AssessmentTypeSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class GradeViewSet(StandardModelViewSet):
    queryset = Grade.objects.filter(is_deleted=False).select_related("subject_group", "student", "assessment_type", "lesson_session", "graded_by")
    serializer_class = GradeSerializer
    permission_classes = [StudentOwnDataPermission]
    organization_field = "subject_group__organization"
    student_field = "student"


class GradeHistoryViewSet(StandardModelViewSet):
    queryset = GradeHistory.objects.filter(is_deleted=False).select_related("grade", "changed_by")
    serializer_class = GradeHistorySerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "grade__subject_group__organization"


class AppealViewSet(StandardModelViewSet):
    queryset = Appeal.objects.filter(is_deleted=False).select_related("grade", "student", "reviewed_by")
    serializer_class = AppealSerializer
    permission_classes = [StudentOwnDataPermission]
    organization_field = "grade__subject_group__organization"
    student_field = "student"
