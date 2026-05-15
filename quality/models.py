from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from core.models import BaseModel, RiskLevel


class QualityInspection(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="quality_inspections")
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Tekshiruvchi", on_delete=models.PROTECT, related_name="quality_inspections")
    subject_group = models.ForeignKey("academics.SubjectGroup", verbose_name="Fan-guruh", null=True, blank=True, on_delete=models.SET_NULL, related_name="quality_inspections")
    lesson_session = models.ForeignKey("journal.LessonSession", verbose_name="Dars", null=True, blank=True, on_delete=models.SET_NULL, related_name="quality_inspections")
    inspected_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Tekshirilgan o'qituvchi", null=True, blank=True, on_delete=models.SET_NULL, related_name="quality_checked_lessons")
    score = models.DecimalField("Sifat balli", max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("100.00"))])
    content_quality_score = models.DecimalField("Kontent sifati", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    teaching_quality_score = models.DecimalField("Dars sifati", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    assessment_transparency_score = models.DecimalField("Baholash shaffofligi", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    conclusion = models.TextField("Xulosa", blank=True)
    recommendations = models.TextField("Tavsiyalar", blank=True)
    inspected_at = models.DateTimeField("Tekshiruv vaqti", default=timezone.now)

    class Meta:
        verbose_name = "Sifat tekshiruvi"
        verbose_name_plural = "Sifat tekshiruvlari"


class Deficiency(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="deficiencies")
    inspection = models.ForeignKey(QualityInspection, verbose_name="Tekshiruv", null=True, blank=True, on_delete=models.SET_NULL, related_name="deficiencies")
    title = models.CharField("Kamchilik", max_length=255)
    description = models.TextField("Tavsif")
    risk_level = models.CharField("Xavf darajasi", max_length=20, choices=RiskLevel.choices, default=RiskLevel.MEDIUM)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Mas'ul", null=True, blank=True, on_delete=models.SET_NULL, related_name="responsible_deficiencies")
    due_date = models.DateField("Bartaraf etish muddati", null=True, blank=True)
    is_resolved = models.BooleanField("Bartaraf etildimi", default=False)
    resolved_at = models.DateTimeField("Bartaraf etilgan vaqt", null=True, blank=True)
    resolution_comment = models.TextField("Bartaraf etish izohi", blank=True)

    class Meta:
        verbose_name = "Kamchilik"
        verbose_name_plural = "Kamchiliklar"


class Survey(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="surveys")
    title = models.CharField("So'rovnoma nomi", max_length=255)
    description = models.TextField("Izoh", blank=True)
    target_faculty = models.ForeignKey("structure.Faculty", verbose_name="Fakultet", null=True, blank=True, on_delete=models.SET_NULL)
    target_group = models.ForeignKey("structure.Group", verbose_name="Guruh", null=True, blank=True, on_delete=models.SET_NULL)
    is_anonymous = models.BooleanField("Anonimmi", default=True)
    starts_at = models.DateTimeField("Boshlanish vaqti")
    ends_at = models.DateTimeField("Tugash vaqti")
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "So'rovnoma"
        verbose_name_plural = "So'rovnomalar"


class SurveyQuestion(BaseModel):
    class SurveyQuestionType(models.TextChoices):
        RATING = "rating", "Reyting"
        TEXT = "text", "Matn"
        SINGLE = "single", "Bitta tanlov"
        MULTIPLE = "multiple", "Ko'p tanlov"

    survey = models.ForeignKey(Survey, verbose_name="So'rovnoma", on_delete=models.CASCADE, related_name="questions")
    text = models.TextField("Savol")
    question_type = models.CharField("Savol turi", max_length=30, choices=SurveyQuestionType.choices)
    options = models.JSONField("Variantlar", default=list, blank=True)
    order = models.PositiveIntegerField("Tartib", default=1)

    class Meta:
        verbose_name = "So'rovnoma savoli"
        verbose_name_plural = "So'rovnoma savollari"


class SurveyResponse(BaseModel):
    survey = models.ForeignKey(Survey, verbose_name="So'rovnoma", on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(SurveyQuestion, verbose_name="Savol", on_delete=models.CASCADE, related_name="responses")
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Javob beruvchi", null=True, blank=True, on_delete=models.SET_NULL, related_name="survey_responses")
    answer = models.JSONField("Javob", default=dict)
    submitted_at = models.DateTimeField("Yuborilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "So'rovnoma javobi"
        verbose_name_plural = "So'rovnoma javoblari"
