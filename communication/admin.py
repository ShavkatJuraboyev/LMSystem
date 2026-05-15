from django.contrib import admin

from .models import Announcement, DirectMessage, SupportRequest


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "author", "faculty", "department", "group", "publish_at", "expires_at", "is_pinned")
    list_filter = ("organization", "faculty", "department", "group", "is_pinned", "publish_at")
    search_fields = ("title", "body", "author__username", "author__first_name", "author__last_name")
    raw_id_fields = ("organization", "author", "faculty", "department", "group", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "publish_at"


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "subject", "read_at", "created_at")
    list_filter = ("read_at", "created_at")
    search_fields = ("sender__username", "receiver__username", "subject", "body")
    raw_id_fields = ("sender", "receiver", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "request_type", "status", "organization", "author", "assigned_to", "due_date", "closed_at", "created_at")
    list_filter = ("organization", "request_type", "status", "assigned_to", "due_date", "closed_at")
    search_fields = ("title", "body", "response", "author__username", "author__first_name", "author__last_name")
    raw_id_fields = ("organization", "author", "assigned_to", "created_by", "updated_by", "deleted_by")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    date_hierarchy = "created_at"
