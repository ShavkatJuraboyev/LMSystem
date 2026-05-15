from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import BaseModel, ContentStatus, SubmissionStatus


class Assignment(BaseModel):
    subject_group = models.ForeignKey("academics.SubjectGroup", verbose_name="Fan-guruh", on_delete=models.CASCADE, related_name="assignments")
    topic = models.ForeignKey("academics.Topic", verbose_name="Mavzu", null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments")
    title = models.CharField("Topshiriq nomi", max_length=255)
    description = models.TextField("Topshiriq matni")
    attachment = models.FileField("Ilova fayl", upload_to="assignments/%Y/%m/", null=True, blank=True)
    starts_at = models.DateTimeField("Boshlanish vaqti", null=True, blank=True)
    deadline = models.DateTimeField("Topshirish muddati", db_index=True)
    max_score = models.DecimalField("Maksimal ball", max_digits=6, decimal_places=2, default=Decimal("100.00"))
    allow_late_submission = models.BooleanField("Kechikib topshirishga ruxsat", default=False)
    plagiarism_check_required = models.BooleanField("Plagiat tekshiruvi kerakmi", default=False)
    status = models.CharField("Status", max_length=30, choices=ContentStatus.choices, default=ContentStatus.ACTIVE)

    class Meta:
        verbose_name = "Topshiriq"
        verbose_name_plural = "Topshiriqlar"
        indexes = [models.Index(fields=["subject_group", "deadline"])]


class AssignmentSubmission(BaseModel):
    assignment = models.ForeignKey(Assignment, verbose_name="Topshiriq", on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey("accounts.StudentProfile", verbose_name="Talaba", on_delete=models.CASCADE, related_name="assignment_submissions")
    text_answer = models.TextField("Matnli javob", blank=True)
    file = models.FileField("Javob fayli", upload_to="assignment_submissions/%Y/%m/", null=True, blank=True)
    submitted_at = models.DateTimeField("Topshirilgan vaqt", auto_now_add=True)
    status = models.CharField("Status", max_length=30, choices=SubmissionStatus.choices, default=SubmissionStatus.SUBMITTED)
    score = models.DecimalField("Ball", max_digits=6, decimal_places=2, null=True, blank=True)
    feedback = models.TextField("O'qituvchi izohi", blank=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Tekshirgan", null=True, blank=True, on_delete=models.SET_NULL, related_name="checked_submissions")
    checked_at = models.DateTimeField("Tekshirilgan vaqt", null=True, blank=True)
    plagiarism_percent = models.DecimalField("Plagiat foizi", max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Topshiriq javobi"
        verbose_name_plural = "Topshiriq javoblari"
        unique_together = ("assignment", "student")
        indexes = [models.Index(fields=["student", "status"])]


class QuestionBank(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="question_banks")
    subject = models.ForeignKey("academics.Subject", verbose_name="Fan", on_delete=models.CASCADE, related_name="question_banks")
    title = models.CharField("Savollar banki nomi", max_length=255)
    description = models.TextField("Izoh", blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Egasi", on_delete=models.PROTECT, related_name="question_banks")
    is_shared = models.BooleanField("Kafedra bilan ulashilganmi", default=False)

    class Meta:
        verbose_name = "Savollar banki"
        verbose_name_plural = "Savollar banklari"


class Question(BaseModel):
    class QuestionType(models.TextChoices):
        SINGLE = "single", "Bitta javob"
        MULTIPLE = "multiple", "Bir nechta javob"
        TEXT = "text", "Matnli javob"
        FILE = "file", "Faylli javob"
        MATCHING = "matching", "Moslashtirish"

    bank = models.ForeignKey(QuestionBank, verbose_name="Savollar banki", on_delete=models.CASCADE, related_name="questions")
    question_type = models.CharField("Savol turi", max_length=30, choices=QuestionType.choices)
    text = models.TextField("Savol matni")
    image = models.ImageField("Savol rasmi", upload_to="questions/images/%Y/%m/", null=True, blank=True)
    difficulty = models.PositiveSmallIntegerField("Qiyinlik darajasi", default=1)
    score = models.DecimalField("Ball", max_digits=6, decimal_places=2, default=Decimal("1.00"))
    explanation = models.TextField("Izoh", blank=True)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"


class AnswerOption(BaseModel):
    question = models.ForeignKey(Question, verbose_name="Savol", on_delete=models.CASCADE, related_name="options")
    text = models.TextField("Javob varianti")
    is_correct = models.BooleanField("To'g'ri javobmi", default=False)
    order = models.PositiveIntegerField("Tartib", default=1)

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"


class Test(BaseModel):
    subject_group = models.ForeignKey("academics.SubjectGroup", verbose_name="Fan-guruh", on_delete=models.CASCADE, related_name="tests")
    title = models.CharField("Test nomi", max_length=255)
    description = models.TextField("Izoh", blank=True)
    starts_at = models.DateTimeField("Boshlanish vaqti", null=True, blank=True)
    ends_at = models.DateTimeField("Tugash vaqti", null=True, blank=True)
    duration_minutes = models.PositiveIntegerField("Davomiylik daqiqada", default=30)
    max_attempts = models.PositiveSmallIntegerField("Urinishlar soni", default=1)
    shuffle_questions = models.BooleanField("Savollarni aralashtirish", default=True)
    shuffle_options = models.BooleanField("Variantlarni aralashtirish", default=True)
    show_result_immediately = models.BooleanField("Natijani darhol ko'rsatish", default=False)
    status = models.CharField("Status", max_length=30, choices=ContentStatus.choices, default=ContentStatus.DRAFT)

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, verbose_name="Test", on_delete=models.CASCADE, related_name="test_questions")
    question = models.ForeignKey(Question, verbose_name="Savol", on_delete=models.PROTECT, related_name="test_questions")
    order = models.PositiveIntegerField("Tartib", default=1)
    custom_score = models.DecimalField("Maxsus ball", max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Test savoli"
        verbose_name_plural = "Test savollari"
        unique_together = ("test", "question")


class TestAttempt(BaseModel):
    test = models.ForeignKey(Test, verbose_name="Test", on_delete=models.CASCADE, related_name="attempts")
    student = models.ForeignKey("accounts.StudentProfile", verbose_name="Talaba", on_delete=models.CASCADE, related_name="test_attempts")
    attempt_number = models.PositiveSmallIntegerField("Urinish raqami", default=1)
    started_at = models.DateTimeField("Boshlangan vaqt", auto_now_add=True)
    submitted_at = models.DateTimeField("Topshirilgan vaqt", null=True, blank=True)
    score = models.DecimalField("Ball", max_digits=6, decimal_places=2, default=Decimal("0.00"))
    max_score = models.DecimalField("Maksimal ball", max_digits=6, decimal_places=2, default=Decimal("0.00"))
    is_submitted = models.BooleanField("Topshirildimi", default=False)
    ip_address = models.GenericIPAddressField("IP manzil", null=True, blank=True)
    user_agent = models.TextField("Qurilma/Brauzer", blank=True)

    class Meta:
        verbose_name = "Test urinishi"
        verbose_name_plural = "Test urinishlari"
        unique_together = ("test", "student", "attempt_number")


class StudentAnswer(BaseModel):
    attempt = models.ForeignKey(TestAttempt, verbose_name="Urinish", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, verbose_name="Savol", on_delete=models.PROTECT, related_name="student_answers")
    selected_options = models.ManyToManyField(AnswerOption, verbose_name="Tanlangan javoblar", blank=True)
    text_answer = models.TextField("Matnli javob", blank=True)
    file_answer = models.FileField("Faylli javob", upload_to="test_answers/%Y/%m/", null=True, blank=True)
    is_correct = models.BooleanField("To'g'rimi", null=True, blank=True)
    score = models.DecimalField("Ball", max_digits=6, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        verbose_name = "Talaba javobi"
        verbose_name_plural = "Talaba javoblari"
        unique_together = ("attempt", "question")
