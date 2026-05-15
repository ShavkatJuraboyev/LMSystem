from rest_framework import serializers

from academics.models import Curriculum, Subject, CurriculumSubject, SubjectGroup, Topic, LearningContent, ContentView


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class CurriculumSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumSubject
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class SubjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroup
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class LearningContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningContent
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "view_count")


class ContentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentView
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")
