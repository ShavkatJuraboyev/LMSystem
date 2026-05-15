from django.contrib import admin

from .models import (
    Curriculum,
    Subject,
    CurriculumSubject,
    SubjectGroup,
    Topic,
    LearningContent,
    ContentView,
)


class CurriculumSubjectInline(admin.TabularInline):
    model = CurriculumSubject
    extra = 0
    raw_id_fields = ("subject",)
    fields = ("subject", "semester_number", "is_required", "max_score", "passing_score")


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "organization", "specialty", "academic_year", "total_credits", "is_active")
    list_filter = ("organization", "specialty", "academic_year", "is_active")
    search_fields = ("name", "code", "specialty__name", "organization__name")
    raw_id_fields = ("organization", "specialty", "academic_year", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    inlines = (CurriculumSubjectInline,)
    ordering = ("organization", "specialty", "name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "organization",
        "department",
        "credits",
        "total_hours",
        "lecture_hours",
        "practice_hours",
        "lab_hours",
        "independent_hours",
        "is_active",
    )
    list_filter = ("organization", "department", "is_active")
    search_fields = ("name", "code", "department__name", "organization__name")
    raw_id_fields = ("organization", "department", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("organization", "department", "name")


@admin.register(CurriculumSubject)
class CurriculumSubjectAdmin(admin.ModelAdmin):
    list_display = ("curriculum", "subject", "semester_number", "is_required", "max_score", "passing_score")
    list_filter = ("curriculum__organization", "curriculum", "semester_number", "is_required")
    search_fields = ("curriculum__name", "subject__name", "subject__code")
    raw_id_fields = ("curriculum", "subject", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0
    fields = ("title", "lesson_type", "order", "planned_date", "status")
    ordering = ("order",)


@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ("subject", "group", "semester", "main_teacher", "organization", "is_active")
    list_filter = ("organization", "semester", "subject", "group", "is_active")
    search_fields = ("subject__name", "subject__code", "group__name", "main_teacher__username", "main_teacher__first_name", "main_teacher__last_name")
    raw_id_fields = ("organization", "subject", "group", "semester", "main_teacher", "created_by", "updated_by", "deleted_by")
    filter_horizontal = ("assistant_teachers",)
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    inlines = (TopicInline,)
    ordering = ("semester", "group", "subject")


class LearningContentInline(admin.TabularInline):
    model = LearningContent
    extra = 0
    fields = ("title", "content_type", "status", "version", "view_count", "approved_by", "approved_at")
    readonly_fields = ("view_count", "approved_at")
    raw_id_fields = ("approved_by",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "subject_group", "lesson_type", "order", "planned_date", "status")
    list_filter = ("lesson_type", "status", "subject_group__semester", "subject_group__organization")
    search_fields = ("title", "description", "subject_group__subject__name", "subject_group__group__name")
    raw_id_fields = ("subject_group", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    inlines = (LearningContentInline,)
    ordering = ("subject_group", "order")


@admin.register(LearningContent)
class LearningContentAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "content_type", "status", "version", "view_count", "approved_by", "approved_at")
    list_filter = ("content_type", "status", "topic__subject_group__organization", "topic__subject_group__semester")
    search_fields = ("title", "text", "topic__title", "topic__subject_group__subject__name")
    raw_id_fields = ("topic", "approved_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "view_count")
    date_hierarchy = "created_at"


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ("content", "user", "viewed_at", "duration_seconds")
    list_filter = ("viewed_at", "content__content_type", "content__status")
    search_fields = ("content__title", "user__username", "user__first_name", "user__last_name")
    raw_id_fields = ("content", "user", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "viewed_at")
    date_hierarchy = "viewed_at"
