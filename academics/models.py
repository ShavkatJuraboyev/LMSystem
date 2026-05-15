from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models import BaseModel, ContentStatus, LessonType


class Curriculum(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="curriculums")
    specialty = models.ForeignKey("structure.Specialty", verbose_name="Yo'nalish", on_delete=models.CASCADE, related_name="curriculums")
    academic_year = models.ForeignKey("structure.AcademicYear", verbose_name="O'quv yili", on_delete=models.PROTECT, related_name="curriculums")
    name = models.CharField("O'quv reja nomi", max_length=255)
    code = models.CharField("O'quv reja kodi", max_length=80)
    total_credits = models.PositiveSmallIntegerField("Jami kredit", default=0)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "O'quv reja"
        verbose_name_plural = "O'quv rejalar"
        unique_together = ("organization", "code")


class Subject(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="subjects")
    department = models.ForeignKey("structure.Department", verbose_name="Mas'ul kafedra", on_delete=models.PROTECT, related_name="subjects")
    code = models.CharField("Fan kodi", max_length=80)
    name = models.CharField("Fan nomi", max_length=255)
    description = models.TextField("Fan tavsifi", blank=True)
    credits = models.PositiveSmallIntegerField("Kredit", default=0)
    total_hours = models.PositiveIntegerField("Jami soat", default=0)
    lecture_hours = models.PositiveIntegerField("Ma'ruza soati", default=0)
    practice_hours = models.PositiveIntegerField("Amaliy soat", default=0)
    lab_hours = models.PositiveIntegerField("Laboratoriya soati", default=0)
    independent_hours = models.PositiveIntegerField("Mustaqil ta'lim soati", default=0)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        unique_together = ("organization", "code")
        indexes = [models.Index(fields=["department", "is_active"])]

    def __str__(self):
        return self.name


class CurriculumSubject(BaseModel):
    curriculum = models.ForeignKey(Curriculum, verbose_name="O'quv reja", on_delete=models.CASCADE, related_name="curriculum_subjects")
    subject = models.ForeignKey(Subject, verbose_name="Fan", on_delete=models.PROTECT, related_name="curriculum_subjects")
    semester_number = models.PositiveSmallIntegerField("Semestr")
    is_required = models.BooleanField("Majburiy fanmi", default=True)
    max_score = models.DecimalField("Maksimal ball", max_digits=5, decimal_places=2, default=Decimal("100.00"))
    passing_score = models.DecimalField("O'tish balli", max_digits=5, decimal_places=2, default=Decimal("60.00"))

    class Meta:
        verbose_name = "O'quv rejadagi fan"
        verbose_name_plural = "O'quv rejadagi fanlar"
        unique_together = ("curriculum", "subject", "semester_number")


class SubjectGroup(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="subject_groups")
    subject = models.ForeignKey(Subject, verbose_name="Fan", on_delete=models.PROTECT, related_name="subject_groups")
    group = models.ForeignKey("structure.Group", verbose_name="Guruh", on_delete=models.PROTECT, related_name="subject_groups")
    semester = models.ForeignKey("structure.Semester", verbose_name="Semestr", on_delete=models.PROTECT, related_name="subject_groups")
    main_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Asosiy o'qituvchi", on_delete=models.PROTECT, related_name="main_subject_groups")
    assistant_teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Yordamchi o'qituvchilar", blank=True, related_name="assistant_subject_groups")
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Fan-guruh"
        verbose_name_plural = "Fan-guruhlar"
        unique_together = ("subject", "group", "semester")
        indexes = [
            models.Index(fields=["organization", "semester"]),
            models.Index(fields=["main_teacher", "semester"]),
        ]

    def __str__(self):
        return f"{self.subject.name} - {self.group.name}"


class Topic(BaseModel):
    subject_group = models.ForeignKey(SubjectGroup, verbose_name="Fan-guruh", on_delete=models.CASCADE, related_name="topics")
    title = models.CharField("Mavzu", max_length=255)
    description = models.TextField("Tavsif", blank=True)
    lesson_type = models.CharField("Dars turi", max_length=30, choices=LessonType.choices)
    order = models.PositiveIntegerField("Tartib raqami", default=1)
    planned_date = models.DateField("Rejadagi sana", null=True, blank=True)
    status = models.CharField("Status", max_length=30, choices=ContentStatus.choices, default=ContentStatus.DRAFT)

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"
        ordering = ["subject_group", "order"]


class LearningContent(BaseModel):
    class ContentType(models.TextChoices):
        FILE = "file", "Fayl"
        VIDEO = "video", "Video"
        LINK = "link", "Havola"
        TEXT = "text", "Matn"
        PRESENTATION = "presentation", "Prezentatsiya"
        BOOK = "book", "Adabiyot"
        OTHER = "other", "Boshqa"

    topic = models.ForeignKey(Topic, verbose_name="Mavzu", on_delete=models.CASCADE, related_name="contents")
    title = models.CharField("Kontent nomi", max_length=255)
    content_type = models.CharField("Kontent turi", max_length=30, choices=ContentType.choices)
    text = models.TextField("Matn", blank=True)
    file = models.FileField(
        "Fayl",
        upload_to="learning_contents/%Y/%m/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "zip", "mp4", "jpg", "jpeg", "png"])],
    )
    url = models.URLField("Havola", blank=True)
    version = models.PositiveIntegerField("Versiya", default=1)
    status = models.CharField("Status", max_length=30, choices=ContentStatus.choices, default=ContentStatus.DRAFT)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Tasdiqlovchi", null=True, blank=True, on_delete=models.SET_NULL, related_name="approved_contents")
    approved_at = models.DateTimeField("Tasdiqlangan vaqt", null=True, blank=True)
    view_count = models.PositiveIntegerField("Ko'rishlar soni", default=0)

    class Meta:
        verbose_name = "O'quv kontenti"
        verbose_name_plural = "O'quv kontentlari"
        indexes = [models.Index(fields=["topic", "status"])]


class ContentView(BaseModel):
    content = models.ForeignKey(LearningContent, verbose_name="Kontent", on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", on_delete=models.CASCADE, related_name="content_views")
    viewed_at = models.DateTimeField("Ko'rilgan vaqt", auto_now_add=True)
    duration_seconds = models.PositiveIntegerField("Ko'rish davomiyligi", default=0)

    class Meta:
        verbose_name = "Kontent ko'rilishi"
        verbose_name_plural = "Kontent ko'rilishlari"
        unique_together = ("content", "user")
        indexes = [models.Index(fields=["user", "viewed_at"])]
