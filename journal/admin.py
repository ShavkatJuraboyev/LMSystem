from django.contrib import admin

from .models import Schedule, LessonSession, Attendance


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "subject_group",
        "teacher",
        "auditorium",
        "weekday",
        "lesson_type",
        "start_time",
        "end_time",
        "start_date",
        "end_date",
        "is_online",
        "is_active",
    )
    list_filter = ("organization", "weekday", "lesson_type", "teacher", "auditorium", "is_online", "is_active")
    search_fields = (
        "subject_group__subject__name",
        "subject_group__group__name",
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
        "auditorium__name",
    )
    raw_id_fields = ("organization", "subject_group", "teacher", "auditorium", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "start_date"
    ordering = ("weekday", "start_time")


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    raw_id_fields = ("student", "marked_by")
    fields = ("student", "status", "late_minutes", "reason", "marked_by", "marked_at")
    readonly_fields = ("marked_at",)


@admin.register(LessonSession)
class LessonSessionAdmin(admin.ModelAdmin):
    list_display = ("date", "subject_group", "teacher", "lesson_type", "topic", "is_completed", "started_at", "ended_at")
    list_filter = ("date", "lesson_type", "is_completed", "subject_group__organization", "subject_group__semester")
    search_fields = ("subject_group__subject__name", "subject_group__group__name", "teacher__username", "topic__title")
    raw_id_fields = ("schedule", "subject_group", "topic", "teacher", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "date"
    inlines = (AttendanceInline,)
    ordering = ("-date",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("lesson_session", "student", "status", "late_minutes", "marked_by", "marked_at")
    list_filter = ("status", "lesson_session__date", "lesson_session__subject_group__organization", "lesson_session__subject_group__semester")
    search_fields = (
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
        "lesson_session__subject_group__subject__name",
    )
    raw_id_fields = ("lesson_session", "student", "marked_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "marked_at")
    date_hierarchy = "marked_at"
