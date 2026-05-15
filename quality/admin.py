from django.contrib import admin

from .models import (
    QualityInspection,
    Deficiency,
    Survey,
    SurveyQuestion,
    SurveyResponse,
)


class DeficiencyInline(admin.TabularInline):
    model = Deficiency
    extra = 0
    raw_id_fields = ("organization", "responsible")
    fields = ("organization", "title", "risk_level", "responsible", "due_date", "is_resolved", "resolved_at")


@admin.register(QualityInspection)
class QualityInspectionAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "inspector",
        "subject_group",
        "lesson_session",
        "inspected_teacher",
        "score",
        "content_quality_score",
        "teaching_quality_score",
        "assessment_transparency_score",
        "inspected_at",
    )
    list_filter = ("organization", "inspected_at", "subject_group__semester", "inspected_teacher")
    search_fields = (
        "inspector__username",
        "inspected_teacher__username",
        "subject_group__subject__name",
        "conclusion",
        "recommendations",
    )
    raw_id_fields = ("organization", "inspector", "subject_group", "lesson_session", "inspected_teacher", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "inspected_at"
    inlines = (DeficiencyInline,)


@admin.register(Deficiency)
class DeficiencyAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "inspection", "risk_level", "responsible", "due_date", "is_resolved", "resolved_at")
    list_filter = ("organization", "risk_level", "is_resolved", "due_date")
    search_fields = ("title", "description", "responsible__username", "resolution_comment")
    raw_id_fields = ("organization", "inspection", "responsible", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "due_date"


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 0
    fields = ("text", "question_type", "options", "order")


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "target_faculty", "target_group", "is_anonymous", "starts_at", "ends_at", "is_active")
    list_filter = ("organization", "target_faculty", "target_group", "is_anonymous", "is_active", "starts_at")
    search_fields = ("title", "description", "organization__name")
    raw_id_fields = ("organization", "target_faculty", "target_group", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "starts_at"
    inlines = (SurveyQuestionInline,)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("survey", "short_text", "question_type", "order")
    list_filter = ("question_type", "survey__organization")
    search_fields = ("text", "survey__title")
    raw_id_fields = ("survey", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

    @admin.display(description="Savol")
    def short_text(self, obj):
        return obj.text[:80] + ("..." if len(obj.text) > 80 else "")


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ("survey", "question", "respondent", "submitted_at")
    list_filter = ("survey__organization", "submitted_at")
    search_fields = ("survey__title", "question__text", "respondent__username")
    raw_id_fields = ("survey", "question", "respondent", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "submitted_at")
    date_hierarchy = "submitted_at"
