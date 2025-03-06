from django.contrib import admin
from .models import (
    CustomUser, Kafedra, Group, Subject, StudentSubject, 
    Timetable, Attendance, Announcement, Message, 
    Exam, ExamResult
)
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy ma’lumotlar', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Tizim ruxsatlari', {'fields': ('role', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Kafedra)
class KafedraAdmin(admin.ModelAdmin):
    list_display = ('name', 'head')
    search_fields = ('name',)
    list_filter = ('head',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'kafedra')
    search_fields = ('name',)
    list_filter = ('kafedra',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'kafedra')
    search_fields = ('name',)
    list_filter = ('kafedra',)

@admin.register(StudentSubject)
class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject')
    search_fields = ('student__username', 'subject__name')
    list_filter = ('subject',)

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'group', 'day_of_week', 'start_time', 'end_time')
    search_fields = ('subject__name', 'teacher__username', 'group__name')
    list_filter = ('day_of_week', 'group')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'is_present')
    search_fields = ('student__username', 'subject__name')
    list_filter = ('date', 'is_present')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'subject', 'created_at')
    search_fields = ('title', 'teacher__username')
    list_filter = ('created_at', 'subject')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('timestamp',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'group', 'date', 'max_score')
    search_fields = ('title', 'subject__name', 'group__name')
    list_filter = ('date', 'group')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score')
    search_fields = ('exam__title', 'student__username')
    list_filter = ('exam',)
