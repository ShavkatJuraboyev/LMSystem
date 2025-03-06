from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Foydalanuvchi autentifikatsiyasi (kirish, chiqish)
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Bosh sahifa
    path("", views.home, name="home"),

    # Profil sahifalari
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("head-of-department/dashboard/", views.head_of_department_dashboard, name="head_of_department_dashboard"),
    path("dean/dashboard/", views.dean_dashboard, name="dean_dashboard"),
    path("super-admin/dashboard/", views.super_admin_dashboard, name="super_admin_dashboard"),
 
    # Yo‘qlama (attendance)
    path("attendance/take/<int:subject_id>/", views.take_attendance, name="take_attendance"),

    # Dars jadvali (timetable)
    path("timetable/create/", views.create_timetable, name="create_timetable"),

    # E‘lonlar (announcements)
    path("announcement/create/", views.create_announcement, name="create_announcement"),

    # Imtihonlar (exams)
    path("exam/create/", views.create_exam, name="create_exam"),
    path("exam/<int:exam_id>/submit-results/", views.submit_exam_results, name="submit_exam_results"),
    path("exam/results/", views.view_exam_results, name="view_exam_results"),

    # 🔹 Imtihonlar
    path("exam/<int:exam_id>/take/", views.take_exam, name="take_exam"),

    # 🔹 Test yaratish yoki yuklash
    path("exam/create-test/", views.create_test, name="create_test"),
]
