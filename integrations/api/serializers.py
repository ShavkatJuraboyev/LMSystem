from rest_framework import serializers

from integrations.models import IntegrationConfig, IntegrationLog, BackupLog, SystemHealthLog


class IntegrationConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationConfig
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class IntegrationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationLog
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class BackupLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupLog
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class SystemHealthLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemHealthLog
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
