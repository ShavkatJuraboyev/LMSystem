from django.contrib import admin

from .models import (
    Organization,
    Faculty,
    Department,
    Specialty,
    AcademicYear,
    Semester,
    Group,
    Auditorium,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "code", "tin", "phone", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "short_name", "code", "tin", "phone", "email")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    raw_id_fields = ("created_by", "updated_by", "deleted_by")
    ordering = ("name",)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "organization", "dean", "is_active", "created_at")
    list_filter = ("organization", "is_active")
    search_fields = ("name", "code", "organization__name", "dean__username", "dean__first_name", "dean__last_name")
    raw_id_fields = ("organization", "dean", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("organization", "name")


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    raw_id_fields = ("organization", "head")
    fields = ("organization", "name", "code", "head", "is_active")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "organization", "faculty", "head", "is_active", "created_at")
    list_filter = ("organization", "faculty", "is_active")
    search_fields = ("name", "code", "organization__name", "faculty__name", "head__username")
    raw_id_fields = ("organization", "faculty", "head", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("organization", "faculty", "name")


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "organization",
        "faculty",
        "department",
        "education_level",
        "education_form",
        "duration_years",
        "is_active",
    )
    list_filter = ("organization", "faculty", "department", "education_level", "education_form", "is_active")
    search_fields = ("name", "code", "organization__name", "faculty__name", "department__name")
    raw_id_fields = ("organization", "faculty", "department", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("organization", "faculty", "name")


class SemesterInline(admin.TabularInline):
    model = Semester
    extra = 0
    fields = ("organization", "name", "semester_type", "number", "start_date", "end_date", "is_current")
    raw_id_fields = ("organization",)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "start_date", "end_date", "is_current", "created_at")
    list_filter = ("organization", "is_current")
    search_fields = ("name", "organization__name", "organization__code")
    raw_id_fields = ("organization", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "start_date"
    inlines = (SemesterInline,)
    ordering = ("-start_date",)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "academic_year", "semester_type", "number", "start_date", "end_date", "is_current")
    list_filter = ("organization", "academic_year", "semester_type", "is_current")
    search_fields = ("name", "academic_year__name", "organization__name")
    raw_id_fields = ("organization", "academic_year", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "start_date"
    ordering = ("-academic_year__start_date", "number")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "faculty", "department", "specialty", "academic_year", "course", "curator", "is_active")
    list_filter = ("organization", "faculty", "department", "specialty", "academic_year", "course", "is_active")
    search_fields = ("name", "specialty__name", "faculty__name", "curator__username", "curator__first_name", "curator__last_name")
    raw_id_fields = ("organization", "faculty", "department", "specialty", "academic_year", "curator", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("organization", "faculty", "course", "name")


@admin.register(Auditorium)
class AuditoriumAdmin(admin.ModelAdmin):
    list_display = ("name", "building", "organization", "capacity", "has_projector", "has_computers", "is_active")
    list_filter = ("organization", "building", "has_projector", "has_computers", "is_active")
    search_fields = ("name", "building", "organization__name")
    raw_id_fields = ("organization", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("organization", "building", "name")
