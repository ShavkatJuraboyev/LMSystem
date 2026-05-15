from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import BaseModel, RequestStatus


class Announcement(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField("E'lon sarlavhasi", max_length=255)
    body = models.TextField("E'lon matni")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Muallif", on_delete=models.PROTECT, related_name="announcements")
    faculty = models.ForeignKey("structure.Faculty", verbose_name="Fakultet", null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey("structure.Department", verbose_name="Kafedra", null=True, blank=True, on_delete=models.SET_NULL)
    group = models.ForeignKey("structure.Group", verbose_name="Guruh", null=True, blank=True, on_delete=models.SET_NULL)
    publish_at = models.DateTimeField("E'lon qilish vaqti", default=timezone.now)
    expires_at = models.DateTimeField("Tugash vaqti", null=True, blank=True)
    is_pinned = models.BooleanField("Muhim e'lonmi", default=False)

    class Meta:
        verbose_name = "E'lon"
        verbose_name_plural = "E'lonlar"


class DirectMessage(BaseModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Yuboruvchi", on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Qabul qiluvchi", on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField("Mavzu", max_length=255, blank=True)
    body = models.TextField("Xabar matni")
    read_at = models.DateTimeField("O'qilgan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "Ichki xabar"
        verbose_name_plural = "Ichki xabarlar"
        indexes = [models.Index(fields=["receiver", "read_at"])]


class SupportRequest(BaseModel):
    class RequestType(models.TextChoices):
        TECHNICAL = "technical", "Texnik muammo"
        ACADEMIC = "academic", "O'quv jarayoni"
        APPEAL = "appeal", "Apellyatsiya"
        DOCUMENT = "document", "Hujjat"
        OTHER = "other", "Boshqa"

    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="support_requests")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Muallif", on_delete=models.CASCADE, related_name="support_requests")
    request_type = models.CharField("Murojaat turi", max_length=30, choices=RequestType.choices)
    title = models.CharField("Mavzu", max_length=255)
    body = models.TextField("Murojaat matni")
    status = models.CharField("Status", max_length=30, choices=RequestStatus.choices, default=RequestStatus.NEW)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Mas'ul", null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_requests")
    due_date = models.DateTimeField("Ijro muddati", null=True, blank=True)
    closed_at = models.DateTimeField("Yopilgan vaqt", null=True, blank=True)
    response = models.TextField("Javob", blank=True)

    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["author", "status"]),
        ]
