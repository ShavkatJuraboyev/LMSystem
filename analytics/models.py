from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import BaseModel, RiskLevel


class KPISnapshot(BaseModel):
    class ScopeType(models.TextChoices):
        ORGANIZATION = "organization", "Muassasa"
        FACULTY = "faculty", "Fakultet"
        DEPARTMENT = "department", "Kafedra"
        GROUP = "group", "Guruh"
        SUBJECT = "subject", "Fan"
        TEACHER = "teacher", "O'qituvchi"
        STUDENT = "student", "Talaba"

    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="kpi_snapshots")
    scope_type = models.CharField("Kesim turi", max_length=30, choices=ScopeType.choices)
    scope_id = models.UUIDField("Kesim ID", null=True, blank=True)
    period_start = models.DateField("Davr boshi")
    period_end = models.DateField("Davr oxiri")
    attendance_percent = models.DecimalField("Davomad foizi", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    average_score = models.DecimalField("O'rtacha ball", max_digits=6, decimal_places=2, default=Decimal("0.00"))
    debt_count = models.PositiveIntegerField("Akademik qarzdorlik soni", default=0)
    content_completion_percent = models.DecimalField("Kontent to'liqligi", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    teacher_activity_score = models.DecimalField("O'qituvchi faolligi", max_digits=6, decimal_places=2, default=Decimal("0.00"))
    quality_index = models.DecimalField("Sifat indeksi", max_digits=6, decimal_places=2, default=Decimal("0.00"))
    extra = models.JSONField("Qo'shimcha ko'rsatkichlar", default=dict, blank=True)

    class Meta:
        verbose_name = "KPI snapshot"
        verbose_name_plural = "KPI snapshotlar"
        indexes = [
            models.Index(fields=["organization", "scope_type"]),
            models.Index(fields=["period_start", "period_end"]),
        ]


class RiskAlert(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="risk_alerts")
    title = models.CharField("Ogohlantirish", max_length=255)
    description = models.TextField("Tavsif", blank=True)
    risk_level = models.CharField("Xavf darajasi", max_length=20, choices=RiskLevel.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", null=True, blank=True, on_delete=models.SET_NULL, related_name="risk_alerts")
    student = models.ForeignKey("accounts.StudentProfile", verbose_name="Talaba", null=True, blank=True, on_delete=models.SET_NULL, related_name="risk_alerts")
    subject_group = models.ForeignKey("academics.SubjectGroup", verbose_name="Fan-guruh", null=True, blank=True, on_delete=models.SET_NULL, related_name="risk_alerts")
    is_resolved = models.BooleanField("Hal etildimi", default=False)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Hal qilgan", null=True, blank=True, on_delete=models.SET_NULL, related_name="resolved_risk_alerts")
    resolved_at = models.DateTimeField("Hal qilingan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "Risk ogohlantirishi"
        verbose_name_plural = "Risk ogohlantirishlari"
        indexes = [models.Index(fields=["organization", "risk_level", "is_resolved"])]
