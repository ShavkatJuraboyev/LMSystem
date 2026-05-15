from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class UserStatus(models.TextChoices):
    ACTIVE = "active", "Faol"
    INACTIVE = "inactive", "Faol emas"
    BLOCKED = "blocked", "Bloklangan"
    ARCHIVED = "archived", "Arxivlangan"


class Gender(models.TextChoices):
    MALE = "male", "Erkak"
    FEMALE = "female", "Ayol"
    OTHER = "other", "Boshqa"


class EducationForm(models.TextChoices):
    FULL_TIME = "full_time", "Kunduzgi"
    PART_TIME = "part_time", "Sirtqi"
    EVENING = "evening", "Kechki"
    DISTANCE = "distance", "Masofaviy"
    SECOND_SPECIALTY = "second_specialty", "Ikkinchi mutaxassislik"


class EducationLevel(models.TextChoices):
    BACHELOR = "bachelor", "Bakalavr"
    MASTER = "master", "Magistratura"
    PHD = "phd", "Doktorantura"
    COLLEGE = "college", "Kollej/Litsey"


class SemesterType(models.TextChoices):
    FALL = "fall", "Kuzgi"
    SPRING = "spring", "Bahorgi"
    SUMMER = "summer", "Yozgi"


class LessonType(models.TextChoices):
    LECTURE = "lecture", "Ma'ruza"
    PRACTICE = "practice", "Amaliy"
    LAB = "lab", "Laboratoriya"
    SEMINAR = "seminar", "Seminar"
    INDEPENDENT = "independent", "Mustaqil ta'lim"
    EXAM = "exam", "Imtihon"
    CONSULTATION = "consultation", "Konsultatsiya"


class WeekDay(models.IntegerChoices):
    MONDAY = 1, "Dushanba"
    TUESDAY = 2, "Seshanba"
    WEDNESDAY = 3, "Chorshanba"
    THURSDAY = 4, "Payshanba"
    FRIDAY = 5, "Juma"
    SATURDAY = 6, "Shanba"
    SUNDAY = 7, "Yakshanba"


class ContentStatus(models.TextChoices):
    DRAFT = "draft", "Qoralama"
    REVIEW = "review", "Tasdiqlashda"
    RETURNED = "returned", "Qayta ishlashga qaytarildi"
    APPROVED = "approved", "Tasdiqlandi"
    ACTIVE = "active", "Faol"
    ARCHIVED = "archived", "Arxivlangan"


class AttendanceStatus(models.TextChoices):
    PRESENT = "present", "Keldi"
    ABSENT = "absent", "Kelmadi"
    LATE = "late", "Kechikdi"
    EXCUSED = "excused", "Sababli"
    ONLINE = "online", "Masofadan qatnashdi"


class GradeStatus(models.TextChoices):
    DRAFT = "draft", "Qoralama"
    PUBLISHED = "published", "E'lon qilingan"
    CHANGED = "changed", "O'zgartirilgan"
    CANCELLED = "cancelled", "Bekor qilingan"


class SubmissionStatus(models.TextChoices):
    DRAFT = "draft", "Qoralama"
    SUBMITTED = "submitted", "Topshirildi"
    LATE = "late", "Kechikdi"
    REVIEWING = "reviewing", "Tekshirilmoqda"
    GRADED = "graded", "Baholandi"
    RETURNED = "returned", "Qayta topshirishga qaytarildi"
    REJECTED = "rejected", "Rad etildi"


class RequestStatus(models.TextChoices):
    NEW = "new", "Yangi"
    IN_REVIEW = "in_review", "Ko'rib chiqilmoqda"
    NEED_INFO = "need_info", "Qo'shimcha ma'lumot kerak"
    ASSIGNED = "assigned", "Mas'ulga yuborildi"
    RESOLVED = "resolved", "Hal qilindi"
    REJECTED = "rejected", "Rad etildi"
    CLOSED = "closed", "Yopildi"


class DocumentStatus(models.TextChoices):
    DRAFT = "draft", "Loyiha"
    AGREEMENT = "agreement", "Kelishuvda"
    APPROVAL = "approval", "Tasdiqlashda"
    APPROVED = "approved", "Tasdiqlangan"
    CANCELLED = "cancelled", "Bekor qilingan"
    ARCHIVED = "archived", "Arxivlangan"


class ApprovalStatus(models.TextChoices):
    WAITING = "waiting", "Kutilmoqda"
    APPROVED = "approved", "Tasdiqlandi"
    REJECTED = "rejected", "Rad etildi"
    RETURNED = "returned", "Qaytarildi"


class RiskLevel(models.TextChoices):
    LOW = "low", "Past"
    MEDIUM = "medium", "O'rta"
    HIGH = "high", "Yuqori"
    CRITICAL = "critical", "Kritik"


class IntegrationStatus(models.TextChoices):
    PENDING = "pending", "Kutilmoqda"
    SUCCESS = "success", "Muvaffaqiyatli"
    PARTIAL_ERROR = "partial_error", "Qisman xato"
    ERROR = "error", "Xato"
    RETRY = "retry", "Qayta yuborildi"


class UUIDTimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField("Yaratilgan sana", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Yangilangan sana", auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField("O'chirilganmi", default=False, db_index=True)
    deleted_at = models.DateTimeField("O'chirilgan sana", null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="O'chirgan foydalanuvchi",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted_items",
    )

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])


class BaseModel(UUIDTimeStampedModel, SoftDeleteModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Yaratgan foydalanuvchi",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_items",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Yangilagan foydalanuvchi",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_items",
    )

    class Meta:
        abstract = True
