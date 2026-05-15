from django.contrib import admin

from .models import (
    Assignment,
    AssignmentSubmission,
    QuestionBank,
    Question,
    AnswerOption,
    Test,
    TestQuestion,
    TestAttempt,
    StudentAnswer,
)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "subject_group", "deadline", "max_score", "allow_late_submission", "plagiarism_check_required", "status")
    list_filter = ("status", "allow_late_submission", "plagiarism_check_required", "subject_group__organization", "subject_group__semester")
    search_fields = ("title", "description", "subject_group__subject__name", "subject_group__group__name")
    raw_id_fields = ("subject_group", "topic", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "deadline"


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "status", "score", "checked_by", "submitted_at", "checked_at", "plagiarism_percent")
    list_filter = ("status", "submitted_at", "checked_at", "assignment__subject_group__organization")
    search_fields = ("assignment__title", "student__student_id", "student__user__first_name", "student__user__last_name", "feedback")
    raw_id_fields = ("assignment", "student", "checked_by", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "submitted_at")
    date_hierarchy = "submitted_at"


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "organization", "owner", "is_shared", "created_at")
    list_filter = ("organization", "subject", "is_shared")
    search_fields = ("title", "description", "subject__name", "owner__username")
    raw_id_fields = ("organization", "subject", "owner", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 2
    fields = ("text", "is_correct", "order")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_text", "bank", "question_type", "difficulty", "score", "is_active")
    list_filter = ("question_type", "difficulty", "is_active", "bank__organization", "bank__subject")
    search_fields = ("text", "bank__title", "bank__subject__name")
    raw_id_fields = ("bank", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    inlines = (AnswerOptionInline,)

    @admin.display(description="Savol")
    def short_text(self, obj):
        return obj.text[:80] + ("..." if len(obj.text) > 80 else "")


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ("question", "short_text", "is_correct", "order")
    list_filter = ("is_correct",)
    search_fields = ("text", "question__text")
    raw_id_fields = ("question", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

    @admin.display(description="Javob")
    def short_text(self, obj):
        return obj.text[:80] + ("..." if len(obj.text) > 80 else "")


class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 0
    raw_id_fields = ("question",)
    fields = ("question", "order", "custom_score")


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "subject_group", "starts_at", "ends_at", "duration_minutes", "max_attempts", "status")
    list_filter = ("status", "subject_group__organization", "subject_group__semester", "shuffle_questions", "shuffle_options")
    search_fields = ("title", "description", "subject_group__subject__name", "subject_group__group__name")
    raw_id_fields = ("subject_group", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "starts_at"
    inlines = (TestQuestionInline,)


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ("test", "question", "order", "custom_score")
    list_filter = ("test__subject_group__organization", "test")
    search_fields = ("test__title", "question__text")
    raw_id_fields = ("test", "question")


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ("test", "student", "attempt_number", "score", "max_score", "is_submitted", "started_at", "submitted_at")
    list_filter = ("is_submitted", "started_at", "submitted_at", "test__subject_group__organization")
    search_fields = ("test__title", "student__student_id", "student__user__first_name", "student__user__last_name")
    raw_id_fields = ("test", "student", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "started_at")
    date_hierarchy = "started_at"


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "is_correct", "score")
    list_filter = ("is_correct",)
    search_fields = ("attempt__student__student_id", "question__text", "text_answer")
    raw_id_fields = ("attempt", "question", "created_by", "updated_by", "deleted_by")
    filter_horizontal = ("selected_options",)
    readonly_fields = ("created_at", "updated_at", "deleted_at")
