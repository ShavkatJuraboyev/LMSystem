from rest_framework import serializers

from analytics.models import KPISnapshot, RiskAlert


class KPISnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPISnapshot
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class RiskAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAlert
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")
