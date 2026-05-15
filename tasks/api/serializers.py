from rest_framework import serializers

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


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "submitted_at")


class QuestionBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class TestAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttempt
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "started_at")


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")
