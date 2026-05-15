from __future__ import annotations

from decimal import Decimal

from django.db import models

from core.models import BaseModel, IntegrationStatus, UUIDTimeStampedModel


class IntegrationConfig(BaseModel):
    class IntegrationType(models.TextChoices):
        HEMIS = "hemis", "HEMIS"
        ONE_ID = "one_id", "OneID"
        SMS = "sms", "SMS provayder"
        EMAIL = "email", "Elektron pochta"
        E_SIGNATURE = "e_signature", "Elektron raqamli imzo"
        ANTIPLAGIAT = "antiplagiat", "Antiplagiat"
        STORAGE = "storage", "Fayl saqlash"
        BI = "bi", "BI/Analitika"
        OTHER = "other", "Boshqa"

    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.CASCADE, related_name="integration_configs")
    integration_type = models.CharField("Integratsiya turi", max_length=40, choices=IntegrationType.choices)
    name = models.CharField("Nomi", max_length=150)
    base_url = models.URLField("Asosiy URL", blank=True)
    is_active = models.BooleanField("Faolmi", default=False)
    config = models.JSONField("Sozlamalar", default=dict, blank=True)
    last_checked_at = models.DateTimeField("Oxirgi tekshiruv", null=True, blank=True)

    class Meta:
        verbose_name = "Integratsiya sozlamasi"
        verbose_name_plural = "Integratsiya sozlamalari"
        unique_together = ("organization", "integration_type", "name")


class IntegrationLog(UUIDTimeStampedModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.SET_NULL, related_name="integration_logs")
    integration = models.ForeignKey(IntegrationConfig, verbose_name="Integratsiya", null=True, blank=True, on_delete=models.SET_NULL, related_name="logs")
    direction = models.CharField("Yo'nalish", max_length=20, choices=[("in", "Kirish"), ("out", "Chiqish")])
    endpoint = models.CharField("Endpoint", max_length=255, blank=True)
    request_payload = models.JSONField("So'rov", default=dict, blank=True)
    response_payload = models.JSONField("Javob", default=dict, blank=True)
    status = models.CharField("Status", max_length=30, choices=IntegrationStatus.choices)
    status_code = models.PositiveSmallIntegerField("HTTP status", null=True, blank=True)
    error_message = models.TextField("Xatolik", blank=True)
    duration_ms = models.PositiveIntegerField("Davomiylik ms", default=0)

    class Meta:
        verbose_name = "Integratsiya logi"
        verbose_name_plural = "Integratsiya loglari"
        indexes = [models.Index(fields=["integration", "status", "created_at"])]


class BackupLog(UUIDTimeStampedModel):
    class BackupType(models.TextChoices):
        FULL = "full", "To'liq"
        INCREMENTAL = "incremental", "Inkremental"

    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.SET_NULL, related_name="backup_logs")
    backup_type = models.CharField("Backup turi", max_length=30, choices=BackupType.choices)
    file_path = models.CharField("Fayl manzili", max_length=500, blank=True)
    file_size_mb = models.DecimalField("Hajm MB", max_digits=10, decimal_places=2, default=Decimal("0.00"))
    is_success = models.BooleanField("Muvaffaqiyatlimi", default=False)
    error_message = models.TextField("Xatolik", blank=True)
    started_at = models.DateTimeField("Boshlangan vaqt")
    finished_at = models.DateTimeField("Tugagan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "Zaxira nusxa logi"
        verbose_name_plural = "Zaxira nusxa loglari"


class SystemHealthLog(UUIDTimeStampedModel):
    cpu_percent = models.DecimalField("CPU %", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    memory_percent = models.DecimalField("RAM %", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    disk_percent = models.DecimalField("Disk %", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    db_status = models.CharField("DB holati", max_length=50, default="ok")
    queue_size = models.PositiveIntegerField("Navbat uzunligi", default=0)
    active_users = models.PositiveIntegerField("Faol foydalanuvchilar", default=0)
    response_time_ms = models.PositiveIntegerField("Javob vaqti ms", default=0)
    extra = models.JSONField("Qo'shimcha", default=dict, blank=True)

    class Meta:
        verbose_name = "Tizim holati logi"
        verbose_name_plural = "Tizim holati loglari"
