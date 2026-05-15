from django.contrib import admin

from .models import AuditLog, LoginHistory, ExportLog, SecurityEvent


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "organization", "module", "action", "object_type", "object_id", "result", "ip_address")
    list_filter = ("organization", "module", "action", "result", "created_at")
    search_fields = ("user__username", "module", "action", "object_type", "object_id", "ip_address")
    raw_id_fields = ("user", "organization")
    readonly_fields = (
        "id",
        "user",
        "organization",
        "role_code",
        "action",
        "module",
        "object_type",
        "object_id",
        "old_values",
        "new_values",
        "result",
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("logged_at", "user", "username", "organization", "is_success", "failure_reason", "ip_address", "city", "country")
    list_filter = ("organization", "is_success", "logged_at")
    search_fields = ("user__username", "username", "ip_address", "failure_reason", "city", "country")
    raw_id_fields = ("user", "organization")
    readonly_fields = (
        "id",
        "user",
        "username",
        "organization",
        "is_success",
        "failure_reason",
        "ip_address",
        "user_agent",
        "country",
        "city",
        "logged_at",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "logged_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ExportLog)
class ExportLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "organization", "report_type", "file_format", "row_count", "ip_address")
    list_filter = ("organization", "report_type", "file_format", "created_at")
    search_fields = ("user__username", "report_type", "file_format", "ip_address")
    raw_id_fields = ("user", "organization")
    readonly_fields = ("id", "user", "organization", "report_type", "file_format", "filters", "row_count", "ip_address", "created_at", "updated_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "organization", "user", "event_type", "risk_level", "is_resolved", "resolved_by", "resolved_at", "ip_address")
    list_filter = ("organization", "event_type", "risk_level", "is_resolved", "created_at")
    search_fields = ("user__username", "description", "ip_address")
    raw_id_fields = ("organization", "user", "resolved_by")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
