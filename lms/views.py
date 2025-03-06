import random
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, Kafedra, Subject, Attendance, Timetable, Announcement, Exam, ExamResult, Group
from .forms import AttendanceForm, TimetableForm, AnnouncementForm, ExamForm, ExamResultForm


def login_decorator(func):
    return login_required(func, login_url='login')

# 🔹 Bosh sahifa
@login_decorator
def home(request):
    return render(request, "home.html")

# 🔹 Login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Foydalanuvchi roliga qarab yo'naltirish
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "teacher":
                return redirect("teacher_dashboard")
            elif user.role == "head_of_department":
                return redirect("head_of_department_dashboard")
            elif user.role == "dean":
                return redirect("dean_dashboard")
            elif user.role == "super_admin":
                return redirect("super_admin_dashboard")
            else:
                messages.error(request, "Noto'g'ri foydalanuvchi roli.")
                return redirect("login")

        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri.")

    return render(request, "login.html")


# 🔹 Logout
@login_decorator
def user_logout(request):
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz.")
    return redirect("login")
 

# 🔹 Talaba profili (o‘z fanlari va o‘qituvchilarini ko‘rishi mumkin)
@login_decorator
def student_dashboard(request):
    student_subjects = Subject.objects.filter(studentsubject__student=request.user)
    teachers = CustomUser.objects.filter(subject__studentsubject__student=request.user, role="teacher").distinct()
    attendance_records = Attendance.objects.filter(student=request.user)
    
    context = {
        "subjects": student_subjects,
        "teachers": teachers,
        "attendance_records": attendance_records,
    }
    return render(request, "student_dashboard.html", context)

# 🔹 O‘qituvchi profili (faqat o‘ziga tegishli fanlar, dars jadvali, imtihon va e’lonlarni ko‘radi)
@login_decorator
def teacher_dashboard(request):
    subjects = Subject.objects.filter(teachers=request.user)
    timetables = Timetable.objects.filter(teacher=request.user)
    exams = Exam.objects.filter(subject__in=subjects)
    announcements = Announcement.objects.filter(teacher=request.user)
    groups = Group.objects.filter(timetables__teacher=request.user).distinct()  # O‘ziga tegishli guruhlarni olish
    
    context = {
        "subjects": subjects,
        "timetables": timetables,
        "exams": exams,
        "announcements": announcements,
        "groups": groups,
    }
    return render(request, "teacher_dashboard.html", context)


# 🔹 Kafedra mudiri profili
@login_decorator
def head_of_department_dashboard(request):
    kafedra = request.user.kafedra
    teachers = CustomUser.objects.filter(kafedra=kafedra, role="teacher")
    
    context = {
        "kafedra": kafedra,
        "teachers": teachers,
    }
    return render(request, "head_of_department_dashboard.html", context)


# 🔹 Dekan profili
@login_decorator
def dean_dashboard(request):
    kafedralar = Kafedra.objects.filter(head__kafedra__head=request.user)
    
    context = {
        "kafedralar": kafedralar,
    }
    return render(request, "dean_dashboard.html", context)


# 🔹 Super Admin paneli
@login_decorator
def super_admin_dashboard(request):
    users = CustomUser.objects.all()
    
    context = {
        "users": users,
    }
    return render(request, "super_admin_dashboard.html", context)


# 🔹 Yo‘qlama olish
@login_decorator
def take_attendance(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
     
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yo‘qlama saqlandi!")
            return redirect("teacher_dashboard")
    else:
        form = AttendanceForm()
    
    return render(request, "take_attendance.html", {"form": form, "subject": subject})


# 🔹 Dars jadvali yaratish (faqat dekan ruxsatiga ega bo‘lishi kerak)
@login_decorator
def create_timetable(request):
    if request.user.role != "dean":
        messages.error(request, "Sizda bu amalni bajarish uchun ruxsat yo‘q!")
        return redirect("home")

    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dars jadvali yaratildi!")
            return redirect("dean_dashboard")
    else:
        form = TimetableForm()

    return render(request, "create_timetable.html", {"form": form})


# 🔹 E’lon qo‘shish (faqat o‘ziga tegishli e’lonlarni yaratadi)
@login_decorator
def create_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.teacher = request.user
            announcement.created_at = timezone.now()
            announcement.save()
            messages.success(request, "E’lon qo‘shildi!")
            return redirect("teacher_dashboard")
    else:
        form = AnnouncementForm()

    return render(request, "create_announcement.html", {"form": form})




# 🔹 Imtihon yaratish (faqat o‘qituvchilar yaratishi mumkin)
@login_decorator
def create_exam(request):
    if request.user.role != "teacher":
        messages.error(request, "Sizda bu amalni bajarish uchun ruxsat yo‘q!")
        return redirect("home")

    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            messages.success(request, "Imtihon qo‘shildi!")
            return redirect("teacher_dashboard")
    else: 
        form = ExamForm()

    return render(request, "create_exam.html", {"form": form})

# 🔹 Test yaratish yoki yuklash
@login_decorator
def create_test(request):
    if request.user.role != "teacher":
        messages.error(request, "Sizda bu amalni bajarish uchun ruxsat yo‘q!")
        return redirect("home")
    
    # Faqat ushbu o‘qituvchiga tegishli bo‘lgan imtihonlarni olish
    exams = Exam.objects.filter(subject__teachers=request.user)  # O‘qituvchiga tegishli imtihonlar

    if request.method == "POST":
        exam_id = request.POST.get("exam")
        exam = get_object_or_404(Exam, id=exam_id)
        
        # Agar test .txt fayl orqali yuklanayotgan bo‘lsa
        if "test_file" in request.FILES:
            file = request.FILES["test_file"]
            test_questions = file.read().decode("utf-8").split("\n")
            exam.test_questions = "\n".join(test_questions)
            exam.save()
            messages.success(request, "Test savollari yuklandi!")
            return redirect("teacher_dashboard")

    return render(request, "create_test.html", {"exams": exams})  # `context` ga `exams` ni qo'shish


# 🔹 Talaba uchun imtihon topshirish (tasodifiy savollar tanlanadi)
@login_decorator
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Test savollarini tasodifiy tartibda olish
    test_questions = exam.test_questions.split("\n")
    random.shuffle(test_questions)
    selected_questions = test_questions[:10]  # Faqat 10 ta savol chiqarish
    
    if request.method == "POST":
        total_score = 0
        for i in range(10):
            correct_answer = request.POST.get(f"question_{i}")
            if correct_answer == "to‘g‘ri":
                total_score += 10  # Har bir savol 10 ball
    
        ExamResult.objects.create(exam=exam, student=request.user, score=total_score)
        messages.success(request, f"Imtihon topshirildi! Siz {total_score} ball oldingiz.")
        return redirect("student_dashboard")

    context = {
        "exam": exam,
        "questions": selected_questions,
    }
    return render(request, "take_exam.html", context)


# 🔹 Imtihon natijalarini kiritish
@login_decorator
def submit_exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == "POST":
        form = ExamResultForm(request.POST)
        if form.is_valid():
            exam_result = form.save(commit=False)
            exam_result.exam = exam
            exam_result.save()
            messages.success(request, "Natijalar kiritildi!")
            return redirect("teacher_dashboard")
    else:
        form = ExamResultForm()
    
    return render(request, "submit_exam_results.html", {"form": form, "exam": exam})


# 🔹 Barcha imtihon natijalarini ko‘rish
@login_decorator
def view_exam_results(request):
    results = ExamResult.objects.all()
    
    context = {
        "results": results,
    }
    return render(request, "view_exam_results.html", context)
