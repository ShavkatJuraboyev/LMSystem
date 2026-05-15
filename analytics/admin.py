from django.contrib import admin

from .models import KPISnapshot, RiskAlert


@admin.register(KPISnapshot)
class KPISnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "scope_type",
        "scope_id",
        "period_start",
        "period_end",
        "attendance_percent",
        "average_score",
        "debt_count",
        "content_completion_percent",
        "teacher_activity_score",
        "quality_index",
    )
    list_filter = ("organization", "scope_type", "period_start", "period_end")
    search_fields = ("organization__name", "organization__code")
    raw_id_fields = ("organization", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "period_start"


@admin.register(RiskAlert)
class RiskAlertAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "risk_level", "user", "student", "subject_group", "is_resolved", "resolved_by", "resolved_at", "created_at")
    list_filter = ("organization", "risk_level", "is_resolved", "resolved_at", "created_at")
    search_fields = ("title", "description", "user__username", "student__student_id", "subject_group__subject__name")
    raw_id_fields = ("organization", "user", "student", "subject_group", "resolved_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"
