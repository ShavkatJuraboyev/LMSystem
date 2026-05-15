from core.api.mixins import StandardModelViewSet
from core.api.permissions import TeacherOwnSubjectPermission, StudentOwnDataPermission

from tasks.models import (
    Assignment,
    AssignmentSubmission,
    QuestionBank,
    Question,
    AnswerOption,
    Test,
    TestQuestion,
    TestAttempt,
    StudentAnswer,
)
from .serializers import (
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    QuestionBankSerializer,
    QuestionSerializer,
    AnswerOptionSerializer,
    TestSerializer,
    TestQuestionSerializer,
    TestAttemptSerializer,
    StudentAnswerSerializer,
)


class AssignmentViewSet(StandardModelViewSet):
    queryset = Assignment.objects.filter(is_deleted=False).select_related("subject_group", "topic")
    serializer_class = AssignmentSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "subject_group__organization"


class AssignmentSubmissionViewSet(StandardModelViewSet):
    queryset = AssignmentSubmission.objects.filter(is_deleted=False).select_related("assignment", "student", "checked_by")
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [StudentOwnDataPermission]
    organization_field = "assignment__subject_group__organization"
    student_field = "student"


class QuestionBankViewSet(StandardModelViewSet):
    queryset = QuestionBank.objects.filter(is_deleted=False).select_related("organization", "subject", "owner")
    serializer_class = QuestionBankSerializer
    permission_classes = [TeacherOwnSubjectPermission]


class QuestionViewSet(StandardModelViewSet):
    queryset = Question.objects.filter(is_deleted=False).select_related("bank")
    serializer_class = QuestionSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "bank__organization"


class AnswerOptionViewSet(StandardModelViewSet):
    queryset = AnswerOption.objects.filter(is_deleted=False).select_related("question")
    serializer_class = AnswerOptionSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "question__bank__organization"


class TestViewSet(StandardModelViewSet):
    queryset = Test.objects.filter(is_deleted=False).select_related("subject_group")
    serializer_class = TestSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "subject_group__organization"


class TestQuestionViewSet(StandardModelViewSet):
    queryset = TestQuestion.objects.all().select_related("test", "question")
    serializer_class = TestQuestionSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "test__subject_group__organization"


class TestAttemptViewSet(StandardModelViewSet):
    queryset = TestAttempt.objects.filter(is_deleted=False).select_related("test", "student")
    serializer_class = TestAttemptSerializer
    permission_classes = [StudentOwnDataPermission]
    organization_field = "test__subject_group__organization"
    student_field = "student"


class StudentAnswerViewSet(StandardModelViewSet):
    queryset = StudentAnswer.objects.filter(is_deleted=False).select_related("attempt", "question")
    serializer_class = StudentAnswerSerializer
    permission_classes = [StudentOwnDataPermission]
    organization_field = "attempt__test__subject_group__organization"
    student_field = "attempt__student"
