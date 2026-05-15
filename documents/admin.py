from django.contrib import admin

from .models import OfficialDocument, DocumentApproval


class DocumentApprovalInline(admin.TabularInline):
    model = DocumentApproval
    extra = 0
    raw_id_fields = ("approver",)
    fields = ("approver", "order", "status", "comment", "acted_at")


@admin.register(OfficialDocument)
class OfficialDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "document_type", "number", "organization", "status", "author", "signed_by", "signed_at", "created_at")
    list_filter = ("organization", "document_type", "status", "signed_at", "created_at")
    search_fields = ("title", "number", "body", "author__username", "signed_by__username", "e_signature_id")
    raw_id_fields = ("organization", "author", "signed_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"
    inlines = (DocumentApprovalInline,)


@admin.register(DocumentApproval)
class DocumentApprovalAdmin(admin.ModelAdmin):
    list_display = ("document", "approver", "order", "status", "acted_at")
    list_filter = ("status", "acted_at", "document__organization", "document__document_type")
    search_fields = ("document__title", "document__number", "approver__username", "comment")
    raw_id_fields = ("document", "approver", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "acted_at"
