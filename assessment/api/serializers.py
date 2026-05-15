from rest_framework import serializers

from assessment.models import AssessmentType, Grade, GradeHistory, Appeal


class AssessmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentType
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "graded_at")


class GradeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeHistory
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "changed_at")


class AppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")
