from rest_framework import serializers

from documents.models import OfficialDocument, DocumentApproval


class OfficialDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialDocument
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class DocumentApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentApproval
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")
