from django.contrib import admin

from .models import AssessmentType, Grade, GradeHistory, Appeal


@admin.register(AssessmentType)
class AssessmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "organization", "max_score", "weight_percent", "is_final", "is_active")
    list_filter = ("organization", "is_final", "is_active")
    search_fields = ("name", "code", "organization__name")
    raw_id_fields = ("organization", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")


class GradeHistoryInline(admin.TabularInline):
    model = GradeHistory
    extra = 0
    raw_id_fields = ("changed_by",)
    fields = ("old_score", "new_score", "reason", "changed_by", "changed_at")
    readonly_fields = ("changed_at",)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject_group", "assessment_type", "score", "max_score", "status", "graded_by", "graded_at")
    list_filter = ("status", "assessment_type", "subject_group__organization", "subject_group__semester", "graded_at")
    search_fields = (
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
        "subject_group__subject__name",
        "subject_group__group__name",
        "graded_by__username",
    )
    raw_id_fields = ("subject_group", "student", "assessment_type", "lesson_session", "graded_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "graded_at")
    date_hierarchy = "graded_at"
    inlines = (GradeHistoryInline,)


@admin.register(GradeHistory)
class GradeHistoryAdmin(admin.ModelAdmin):
    list_display = ("grade", "old_score", "new_score", "changed_by", "changed_at")
    list_filter = ("changed_at",)
    search_fields = ("grade__student__student_id", "changed_by__username", "reason")
    raw_id_fields = ("grade", "changed_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "changed_at")
    date_hierarchy = "changed_at"


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ("student", "grade", "status", "reviewed_by", "reviewed_at", "created_at")
    list_filter = ("status", "reviewed_at", "created_at")
    search_fields = ("student__student_id", "student__user__first_name", "student__user__last_name", "reason", "response")
    raw_id_fields = ("grade", "student", "reviewed_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"
