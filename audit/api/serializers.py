from rest_framework import serializers

from audit.models import AuditLog, LoginHistory, ExportLog, SecurityEvent


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "organization",
            "role_code",
            "action",
            "module",
            "object_type",
            "object_id",
            "old_values",
            "new_values",
            "result",
            "ip_address",
            "user_agent",
            "created_at",
            "updated_at",
        )


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "username",
            "organization",
            "is_success",
            "failure_reason",
            "ip_address",
            "user_agent",
            "country",
            "city",
            "logged_at",
            "created_at",
            "updated_at",
        )


class ExportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportLog
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "organization",
            "report_type",
            "file_format",
            "filters",
            "row_count",
            "ip_address",
            "created_at",
            "updated_at",
        )


class SecurityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )