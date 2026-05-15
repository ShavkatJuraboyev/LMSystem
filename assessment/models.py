from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

from core.models import BaseModel, GradeStatus, RequestStatus


class AssessmentType(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="assessment_types")
    name = models.CharField("Nazorat turi", max_length=150)
    code = models.CharField("Kod", max_length=50)
    max_score = models.DecimalField("Maksimal ball", max_digits=6, decimal_places=2)
    weight_percent = models.DecimalField("Ulush foizi", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    is_final = models.BooleanField("Yakuniy nazoratmi", default=False)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Baholash turi"
        verbose_name_plural = "Baholash turlari"
        unique_together = ("organization", "code")


class Grade(BaseModel):
    subject_group = models.ForeignKey("academics.SubjectGroup", verbose_name="Fan-guruh", on_delete=models.PROTECT, related_name="grades")
    student = models.ForeignKey("accounts.StudentProfile", verbose_name="Talaba", on_delete=models.CASCADE, related_name="grades")
    assessment_type = models.ForeignKey(AssessmentType, verbose_name="Nazorat turi", on_delete=models.PROTECT, related_name="grades")
    lesson_session = models.ForeignKey("journal.LessonSession", verbose_name="Dars", null=True, blank=True, on_delete=models.SET_NULL, related_name="grades")
    score = models.DecimalField("Ball", max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    max_score = models.DecimalField("Maksimal ball", max_digits=6, decimal_places=2)
    comment = models.TextField("Izoh", blank=True)
    status = models.CharField("Status", max_length=30, choices=GradeStatus.choices, default=GradeStatus.PUBLISHED)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Baholagan", on_delete=models.PROTECT, related_name="given_grades")
    graded_at = models.DateTimeField("Baholangan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Baho"
        verbose_name_plural = "Baholar"
        indexes = [
            models.Index(fields=["student", "subject_group"]),
            models.Index(fields=["subject_group", "assessment_type"]),
            models.Index(fields=["graded_at"]),
        ]


class GradeHistory(BaseModel):
    grade = models.ForeignKey(Grade, verbose_name="Baho", on_delete=models.CASCADE, related_name="history")
    old_score = models.DecimalField("Eski ball", max_digits=6, decimal_places=2, null=True, blank=True)
    new_score = models.DecimalField("Yangi ball", max_digits=6, decimal_places=2)
    reason = models.TextField("O'zgarish sababi")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="O'zgartirgan", on_delete=models.PROTECT, related_name="grade_changes")
    changed_at = models.DateTimeField("O'zgartirilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Baho o'zgarish tarixi"
        verbose_name_plural = "Baho o'zgarish tarixi"


class Appeal(BaseModel):
    grade = models.ForeignKey(Grade, verbose_name="Baho", on_delete=models.CASCADE, related_name="appeals")
    student = models.ForeignKey("accounts.StudentProfile", verbose_name="Talaba", on_delete=models.CASCADE, related_name="appeals")
    reason = models.TextField("Apellyatsiya sababi")
    status = models.CharField("Status", max_length=30, choices=RequestStatus.choices, default=RequestStatus.NEW)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Ko'rib chiqqan", null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewed_appeals")
    response = models.TextField("Javob", blank=True)
    reviewed_at = models.DateTimeField("Ko'rib chiqilgan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "Apellyatsiya"
        verbose_name_plural = "Apellyatsiyalar"
