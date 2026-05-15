from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import (
    User,
    Module,
    Permission,
    Role,
    RolePermission,
    UserRoleAssignment,
    EmployeeProfile,
    StudentProfile,
)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "full_name",
        "organization",
        "phone",
        "email",
        "status",
        "two_factor_enabled",
        "is_staff",
        "is_active",
        "last_login",
    )
    list_filter = (
        "status",
        "organization",
        "two_factor_enabled",
        "is_staff",
        "is_superuser",
        "is_active",
        "gender",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "middle_name",
        "phone",
        "email",
        "passport_pinfl",
    )
    ordering = ("username",)
    raw_id_fields = ("organization",)
    readonly_fields = (
        "last_login",
        "date_joined",
        "last_activity_at",
        "failed_login_attempts",
    )

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "LMS ma'lumotlari",
            {
                "fields": (
                    "organization",
                    "middle_name",
                    "phone",
                    "passport_pinfl",
                    "birth_date",
                    "gender",
                    "avatar",
                    "status",
                    "two_factor_enabled",
                    "last_password_change",
                    "last_activity_at",
                    "failed_login_attempts",
                )
            },
        ),
    )

    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Qo'shimcha ma'lumotlar",
            {
                "fields": (
                    "organization",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "phone",
                    "email",
                    "status",
                )
            },
        ),
    )

    @admin.display(description="F.I.Sh.")
    def full_name(self, obj):
        return obj.full_name


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name", "description")
    ordering = ("code",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "module", "action")
    list_filter = ("module", "action")
    search_fields = ("code", "name", "module__name")
    autocomplete_fields = ("module",)
    ordering = ("module__code", "action")


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 0
    autocomplete_fields = ("permission",)
    fields = ("permission", "conditions", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "role_type",
        "organization",
        "is_system",
        "is_active",
        "created_at",
    )
    list_filter = ("role_type", "is_system", "is_active", "organization")
    search_fields = ("name", "code", "description", "organization__name")
    raw_id_fields = ("organization", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    inlines = (RolePermissionInline,)
    ordering = ("organization", "role_type", "name")


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "permission", "created_at")
    list_filter = ("role__role_type", "permission__module", "permission__action")
    search_fields = ("role__name", "role__code", "permission__code", "permission__name")
    autocomplete_fields = ("role", "permission")
    readonly_fields = ("created_at",)


@admin.register(UserRoleAssignment)
class UserRoleAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "organization",
        "faculty",
        "department",
        "group",
        "subject",
        "is_active",
        "starts_at",
        "ends_at",
    )
    list_filter = (
        "is_active",
        "role__role_type",
        "organization",
        "faculty",
        "department",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "role__name",
        "role__code",
    )
    raw_id_fields = (
        "user",
        "role",
        "organization",
        "faculty",
        "department",
        "group",
        "subject",
        "created_by",
        "updated_by",
        "deleted_by",
    )
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "organization",
        "faculty",
        "department",
        "position",
        "academic_degree",
        "academic_title",
        "is_teacher",
        "hire_date",
    )
    list_filter = (
        "organization",
        "faculty",
        "department",
        "is_teacher",
        "academic_degree",
        "academic_title",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "employee_id",
        "position",
    )
    raw_id_fields = (
        "user",
        "organization",
        "faculty",
        "department",
        "created_by",
        "updated_by",
        "deleted_by",
    )
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "user",
        "organization",
        "faculty",
        "specialty",
        "group",
        "course",
        "education_form",
        "education_level",
        "admission_year",
        "gpa",
    )
    list_filter = (
        "organization",
        "faculty",
        "specialty",
        "group",
        "course",
        "education_form",
        "education_level",
        "admission_year",
    )
    search_fields = (
        "student_id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__passport_pinfl",
        "group__name",
    )
    raw_id_fields = (
        "user",
        "organization",
        "faculty",
        "department",
        "specialty",
        "group",
        "created_by",
        "updated_by",
        "deleted_by",
    )
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"
