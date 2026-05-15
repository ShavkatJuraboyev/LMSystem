from rest_framework import serializers

from quality.models import QualityInspection, Deficiency, Survey, SurveyQuestion, SurveyResponse


class QualityInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityInspection
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class DeficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deficiency
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class SurveySerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "submitted_at")
