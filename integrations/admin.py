from django.contrib import admin

from .models import IntegrationConfig, IntegrationLog, BackupLog, SystemHealthLog


@admin.register(IntegrationConfig)
class IntegrationConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "integration_type", "organization", "base_url", "is_active", "last_checked_at")
    list_filter = ("integration_type", "organization", "is_active", "last_checked_at")
    search_fields = ("name", "base_url", "organization__name")
    raw_id_fields = ("organization", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")


@admin.register(IntegrationLog)
class IntegrationLogAdmin(admin.ModelAdmin):
    list_display = ("integration", "organization", "direction", "endpoint", "status", "status_code", "duration_ms", "created_at")
    list_filter = ("organization", "integration", "direction", "status", "status_code", "created_at")
    search_fields = ("endpoint", "error_message", "integration__name", "organization__name")
    raw_id_fields = ("organization", "integration")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    list_display = ("organization", "backup_type", "file_size_mb", "is_success", "started_at", "finished_at")
    list_filter = ("organization", "backup_type", "is_success", "started_at", "finished_at")
    search_fields = ("file_path", "error_message", "organization__name")
    raw_id_fields = ("organization",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "started_at"


@admin.register(SystemHealthLog)
class SystemHealthLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "cpu_percent", "memory_percent", "disk_percent", "db_status", "queue_size", "active_users", "response_time_ms")
    list_filter = ("db_status", "created_at")
    search_fields = ("db_status",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
