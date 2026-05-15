from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q

from core.models import AttendanceStatus, BaseModel, LessonType, WeekDay


class Schedule(BaseModel):
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="schedules")
    subject_group = models.ForeignKey("academics.SubjectGroup", verbose_name="Fan-guruh", on_delete=models.CASCADE, related_name="schedules")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="O'qituvchi", on_delete=models.PROTECT, related_name="schedules")
    auditorium = models.ForeignKey("structure.Auditorium", verbose_name="Auditoriya", null=True, blank=True, on_delete=models.SET_NULL, related_name="schedules")
    weekday = models.PositiveSmallIntegerField("Hafta kuni", choices=WeekDay.choices)
    lesson_type = models.CharField("Dars turi", max_length=30, choices=LessonType.choices)
    start_time = models.TimeField("Boshlanish vaqti")
    end_time = models.TimeField("Tugash vaqti")
    start_date = models.DateField("Boshlanish sanasi")
    end_date = models.DateField("Tugash sanasi")
    is_online = models.BooleanField("Onlaynmi", default=False)
    online_url = models.URLField("Onlayn dars havolasi", blank=True)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Dars jadvali"
        verbose_name_plural = "Dars jadvallari"
        indexes = [
            models.Index(fields=["organization", "weekday"]),
            models.Index(fields=["teacher", "weekday"]),
            models.Index(fields=["auditorium", "weekday"]),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(end_time__gt=models.F("start_time")), name="schedule_end_after_start"),
            models.CheckConstraint(condition=Q(end_date__gte=models.F("start_date")), name="schedule_end_date_after_start"),
        ]


class LessonSession(BaseModel):
    schedule = models.ForeignKey(Schedule, verbose_name="Jadval", on_delete=models.PROTECT, related_name="lesson_sessions")
    subject_group = models.ForeignKey("academics.SubjectGroup", verbose_name="Fan-guruh", on_delete=models.PROTECT, related_name="lesson_sessions")
    topic = models.ForeignKey("academics.Topic", verbose_name="Mavzu", null=True, blank=True, on_delete=models.SET_NULL, related_name="lesson_sessions")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="O'qituvchi", on_delete=models.PROTECT, related_name="lesson_sessions")
    date = models.DateField("Dars sanasi", db_index=True)
    lesson_type = models.CharField("Dars turi", max_length=30, choices=LessonType.choices)
    started_at = models.DateTimeField("Boshlangan vaqt", null=True, blank=True)
    ended_at = models.DateTimeField("Tugagan vaqt", null=True, blank=True)
    is_completed = models.BooleanField("Dars o'tildimi", default=False)
    teacher_comment = models.TextField("O'qituvchi izohi", blank=True)

    class Meta:
        verbose_name = "Dars mashg'uloti"
        verbose_name_plural = "Dars mashg'ulotlari"
        unique_together = ("subject_group", "date", "lesson_type", "teacher")
        indexes = [
            models.Index(fields=["date", "is_completed"]),
            models.Index(fields=["subject_group", "date"]),
        ]


class Attendance(BaseModel):
    lesson_session = models.ForeignKey(LessonSession, verbose_name="Dars", on_delete=models.CASCADE, related_name="attendances")
    student = models.ForeignKey("accounts.StudentProfile", verbose_name="Talaba", on_delete=models.CASCADE, related_name="attendances")
    status = models.CharField("Davomad holati", max_length=30, choices=AttendanceStatus.choices)
    late_minutes = models.PositiveSmallIntegerField("Kechikish daqiqasi", default=0)
    reason = models.TextField("Sabab/izoh", blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Belgilagan", on_delete=models.PROTECT, related_name="marked_attendances")
    marked_at = models.DateTimeField("Belgilangan vaqt", auto_now_add=True)
    changed_reason = models.TextField("Tahrir sababi", blank=True)

    class Meta:
        verbose_name = "Davomad"
        verbose_name_plural = "Davomad"
        unique_together = ("lesson_session", "student")
        indexes = [
            models.Index(fields=["student", "status"]),
            models.Index(fields=["lesson_session", "status"]),
        ]
