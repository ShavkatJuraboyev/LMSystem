from __future__ import annotations

from django.conf import settings
from django.db import models

from core.models import RiskLevel, UUIDTimeStampedModel


class AuditLog(UUIDTimeStampedModel):
    class Result(models.TextChoices):
        SUCCESS = "success", "Muvaffaqiyatli"
        FAILED = "failed", "Muvaffaqiyatsiz"
        DENIED = "denied", "Rad etildi"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", null=True, blank=True, on_delete=models.SET_NULL, related_name="audit_logs")
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.SET_NULL, related_name="audit_logs")
    role_code = models.CharField("Rol kodi", max_length=80, blank=True)
    action = models.CharField("Amal", max_length=120)
    module = models.CharField("Modul", max_length=120, blank=True)
    object_type = models.CharField("Obyekt turi", max_length=120, blank=True)
    object_id = models.CharField("Obyekt ID", max_length=120, blank=True)
    old_values = models.JSONField("Eski qiymatlar", default=dict, blank=True)
    new_values = models.JSONField("Yangi qiymatlar", default=dict, blank=True)
    result = models.CharField("Natija", max_length=30, choices=Result.choices, default=Result.SUCCESS)
    ip_address = models.GenericIPAddressField("IP manzil", null=True, blank=True)
    user_agent = models.TextField("Qurilma/Brauzer", blank=True)
    created_at = models.DateTimeField("Vaqt", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Audit log"
        verbose_name_plural = "Audit loglar"
        indexes = [
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["module", "action"]),
            models.Index(fields=["object_type", "object_id"]),
        ]


class LoginHistory(UUIDTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", null=True, blank=True, on_delete=models.SET_NULL, related_name="login_history")
    username = models.CharField("Login", max_length=150, blank=True)
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.SET_NULL)
    is_success = models.BooleanField("Muvaffaqiyatlimi", default=False)
    failure_reason = models.CharField("Xatolik sababi", max_length=255, blank=True)
    ip_address = models.GenericIPAddressField("IP manzil", null=True, blank=True)
    user_agent = models.TextField("Qurilma/Brauzer", blank=True)
    country = models.CharField("Davlat", max_length=100, blank=True)
    city = models.CharField("Shahar", max_length=100, blank=True)
    logged_at = models.DateTimeField("Login vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "Login tarixi"
        verbose_name_plural = "Login tarixi"
        indexes = [
            models.Index(fields=["user", "logged_at"]),
            models.Index(fields=["ip_address", "logged_at"]),
        ]


class ExportLog(UUIDTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", on_delete=models.PROTECT, related_name="export_logs")
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.SET_NULL, related_name="export_logs")
    report_type = models.CharField("Hisobot turi", max_length=100)
    file_format = models.CharField("Fayl formati", max_length=20)
    filters = models.JSONField("Filtrlar", default=dict, blank=True)
    row_count = models.PositiveIntegerField("Qatorlar soni", default=0)
    ip_address = models.GenericIPAddressField("IP manzil", null=True, blank=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Eksport logi"
        verbose_name_plural = "Eksport loglari"


class SecurityEvent(UUIDTimeStampedModel):
    class EventType(models.TextChoices):
        BRUTE_FORCE = "brute_force", "Brute-force"
        SUSPICIOUS_LOGIN = "suspicious_login", "Shubhali login"
        PERMISSION_DENIED = "permission_denied", "Ruxsat rad etildi"
        FILE_BLOCKED = "file_blocked", "Fayl bloklandi"
        MASS_EXPORT = "mass_export", "Ommaviy eksport"
        ROLE_CHANGED = "role_changed", "Rol o'zgardi"
        PASSWORD_CHANGED = "password_changed", "Parol o'zgardi"
        OTHER = "other", "Boshqa"

    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.SET_NULL, related_name="security_events")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", null=True, blank=True, on_delete=models.SET_NULL, related_name="security_events")
    event_type = models.CharField("Hodisa turi", max_length=50, choices=EventType.choices)
    risk_level = models.CharField("Xavf darajasi", max_length=20, choices=RiskLevel.choices, default=RiskLevel.MEDIUM)
    description = models.TextField("Tavsif")
    ip_address = models.GenericIPAddressField("IP manzil", null=True, blank=True)
    user_agent = models.TextField("Qurilma/Brauzer", blank=True)
    is_resolved = models.BooleanField("Hal etildimi", default=False)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Hal qilgan", null=True, blank=True, on_delete=models.SET_NULL, related_name="resolved_security_events")
    resolved_at = models.DateTimeField("Hal qilingan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "Xavfsizlik hodisasi"
        verbose_name_plural = "Xavfsizlik hodisalari"
        indexes = [models.Index(fields=["organization", "event_type", "risk_level"])]
