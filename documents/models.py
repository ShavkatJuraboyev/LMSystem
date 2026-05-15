from __future__ import annotations

from django.conf import settings
from django.db import models

from core.models import ApprovalStatus, BaseModel, DocumentStatus


class OfficialDocument(BaseModel):
    class DocumentType(models.TextChoices):
        ORDER = "order", "Buyruq"
        ACT = "act", "Dalolatnoma"
        REFERENCE = "reference", "Ma'lumotnoma"
        LETTER = "letter", "Xizmat xati"
        TASK = "task", "Topshiriq"
        OTHER = "other", "Boshqa"

    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField("Hujjat turi", max_length=30, choices=DocumentType.choices)
    number = models.CharField("Hujjat raqami", max_length=100, blank=True)
    title = models.CharField("Hujjat nomi", max_length=255)
    body = models.TextField("Hujjat matni", blank=True)
    file = models.FileField("Hujjat fayli", upload_to="official_documents/%Y/%m/", null=True, blank=True)
    status = models.CharField("Status", max_length=30, choices=DocumentStatus.choices, default=DocumentStatus.DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Muallif", on_delete=models.PROTECT, related_name="authored_documents")
    signed_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Imzolagan", null=True, blank=True, on_delete=models.SET_NULL, related_name="signed_documents")
    signed_at = models.DateTimeField("Imzolangan vaqt", null=True, blank=True)
    e_signature_id = models.CharField("ERI identifikatori", max_length=255, blank=True)

    class Meta:
        verbose_name = "Rasmiy hujjat"
        verbose_name_plural = "Rasmiy hujjatlar"
        indexes = [models.Index(fields=["organization", "document_type", "status"])]


class DocumentApproval(BaseModel):
    document = models.ForeignKey(OfficialDocument, verbose_name="Hujjat", on_delete=models.CASCADE, related_name="approvals")
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Tasdiqlovchi", on_delete=models.PROTECT, related_name="document_approvals")
    order = models.PositiveIntegerField("Tasdiqlash tartibi", default=1)
    status = models.CharField("Status", max_length=30, choices=ApprovalStatus.choices, default=ApprovalStatus.WAITING)
    comment = models.TextField("Izoh", blank=True)
    acted_at = models.DateTimeField("Amal bajarilgan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "Hujjat tasdiqlovi"
        verbose_name_plural = "Hujjat tasdiqlovlari"
        unique_together = ("document", "approver", "order")
