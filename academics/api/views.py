from core.api.mixins import StandardModelViewSet
from core.api.permissions import ReadOnlyForManagementWriteForAdmin, TeacherOwnSubjectPermission

from academics.models import Curriculum, Subject, CurriculumSubject, SubjectGroup, Topic, LearningContent, ContentView
from .serializers import (
    CurriculumSerializer,
    SubjectSerializer,
    CurriculumSubjectSerializer,
    SubjectGroupSerializer,
    TopicSerializer,
    LearningContentSerializer, 
    ContentViewSerializer,
)


class CurriculumViewSet(StandardModelViewSet):
    queryset = Curriculum.objects.filter(is_deleted=False).select_related("organization", "specialty", "academic_year")
    serializer_class = CurriculumSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class SubjectViewSet(StandardModelViewSet):
    queryset = Subject.objects.filter(is_deleted=False).select_related("organization", "department")
    serializer_class = SubjectSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]
    department_field = "department"


class CurriculumSubjectViewSet(StandardModelViewSet):
    queryset = CurriculumSubject.objects.filter(is_deleted=False).select_related("curriculum", "subject")
    serializer_class = CurriculumSubjectSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]
    organization_field = "curriculum__organization"


class SubjectGroupViewSet(StandardModelViewSet):
    queryset = SubjectGroup.objects.filter(is_deleted=False).select_related("organization", "subject", "group", "semester", "main_teacher").prefetch_related("assistant_teachers")
    serializer_class = SubjectGroupSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class TopicViewSet(StandardModelViewSet):
    queryset = Topic.objects.filter(is_deleted=False).select_related("subject_group", "subject_group__subject", "subject_group__group")
    serializer_class = TopicSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "subject_group__organization"


class LearningContentViewSet(StandardModelViewSet):
    queryset = LearningContent.objects.filter(is_deleted=False).select_related("topic", "topic__subject_group", "approved_by")
    serializer_class = LearningContentSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "topic__subject_group__organization"


class ContentViewViewSet(StandardModelViewSet):
    queryset = ContentView.objects.filter(is_deleted=False).select_related("content", "user")
    serializer_class = ContentViewSerializer
    permission_classes = [TeacherOwnSubjectPermission]
    organization_field = "content__topic__subject_group__organization"
