from core.api.mixins import StandardModelViewSet
from core.api.permissions import QualityControlPermission

from quality.models import QualityInspection, Deficiency, Survey, SurveyQuestion, SurveyResponse
from .serializers import QualityInspectionSerializer, DeficiencySerializer, SurveySerializer, SurveyQuestionSerializer, SurveyResponseSerializer


class QualityInspectionViewSet(StandardModelViewSet):
    queryset = QualityInspection.objects.filter(is_deleted=False).select_related("organization", "inspector", "subject_group", "lesson_session", "inspected_teacher")
    serializer_class = QualityInspectionSerializer
    permission_classes = [QualityControlPermission]


class DeficiencyViewSet(StandardModelViewSet):
    queryset = Deficiency.objects.filter(is_deleted=False).select_related("organization", "inspection", "responsible")
    serializer_class = DeficiencySerializer
    permission_classes = [QualityControlPermission]


class SurveyViewSet(StandardModelViewSet):
    queryset = Survey.objects.filter(is_deleted=False).select_related("organization", "target_faculty", "target_group")
    serializer_class = SurveySerializer
    permission_classes = [QualityControlPermission]


class SurveyQuestionViewSet(StandardModelViewSet):
    queryset = SurveyQuestion.objects.filter(is_deleted=False).select_related("survey")
    serializer_class = SurveyQuestionSerializer
    permission_classes = [QualityControlPermission]
    organization_field = "survey__organization"


class SurveyResponseViewSet(StandardModelViewSet):
    queryset = SurveyResponse.objects.filter(is_deleted=False).select_related("survey", "question", "respondent")
    serializer_class = SurveyResponseSerializer
    permission_classes = [QualityControlPermission]
    organization_field = "survey__organization"
