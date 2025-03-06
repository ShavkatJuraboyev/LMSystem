from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Foydalanuvchi roli
class UserRole(models.TextChoices):
    STUDENT = "student", "Talaba"
    TEACHER = "teacher", "O‘qituvchi"
    HEAD_OF_DEPARTMENT = "head_of_department", "Kafedra Mudiri"
    DEAN = "dean", "Dekan"
    SUPER_ADMIN = "super_admin", "Super Admin"


# Foydalanuvchi modeli
class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.STUDENT, verbose_name="Foydalanuvchi roli")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    kafedra = models.ForeignKey("Kafedra", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kafedra")

    # Guruhlar va ruxsatlarni qo‘shish
    groups = models.ManyToManyField(Group, blank=True, related_name="custom_users", verbose_name="Guruhlar")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_users", verbose_name="Ruxsatlar")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


# Kafedra modeli
class Kafedra(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kafedra nomi")
    head = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="kafedra_head", verbose_name="Kafedra mudiri")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Kafedralar"
        verbose_name = "Kafedra"


# Guruh modeli (Talabalar uchun)
class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="Guruh nomi")
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE, related_name="groups", verbose_name="Kafedra")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"


# Fan modeli
class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name="Fan nomi")
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE, related_name="subjects", verbose_name="Kafedra")
    teachers = models.ManyToManyField(CustomUser, limit_choices_to={'role': UserRole.TEACHER}, verbose_name="O‘qituvchilar")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Fanlar"
        verbose_name = "Fan"


# Talaba va Fan bog‘lanishi
class StudentSubject(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': UserRole.STUDENT}, verbose_name="Talaba")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}"
    
    class Meta:
        unique_together = ('student', 'subject')
        verbose_name = "Talaba va Fan"
        verbose_name_plural = "Talabalar va Fanlar"


# Dars jadvali
class Timetable(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timetables", verbose_name="Fan")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': UserRole.TEACHER}, verbose_name="O‘qituvchi")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="timetables", verbose_name="Guruh")
    day_of_week = models.CharField(max_length=10, choices=[
        ("Monday", "Dushanba"), ("Tuesday", "Seshanba"), ("Wednesday", "Chorshanba"),
        ("Thursday", "Payshanba"), ("Friday", "Juma"), ("Saturday", "Shanba")
    ], verbose_name="Hafta kuni")
    start_time = models.TimeField(verbose_name="Boshlanish vaqti")
    end_time = models.TimeField(verbose_name="Tugash vaqti")

    def __str__(self):
        return f"{self.subject.name} ({self.day_of_week} {self.start_time} - {self.end_time})"
    
    class Meta:
        verbose_name_plural = "Dars jadvali"
        verbose_name = "Dars jadvali"


# Yo‘qlama tizimi
class Attendance(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': UserRole.STUDENT}, verbose_name="Talaba")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    date = models.DateField(auto_now_add=True, verbose_name="Sana")
    is_present = models.BooleanField(default=False, verbose_name="Qatnashganmi")

    class Meta:
        unique_together = ('student', 'subject', 'date')
        verbose_name = "Yo‘qlama"
        verbose_name_plural = "Yo‘qlamalar"

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}: {'Qatnashdi' if self.is_present else 'Qatnashmadi'}"


# O‘qituvchilar uchun e‘lonlar tizimi
class Announcement(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': UserRole.TEACHER}, verbose_name="O‘qituvchi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="announcements", verbose_name="Fan")
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "E‘lon"
        verbose_name_plural = "E‘lonlar"


# Xabarlar (Chat) tizimi
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="Jo‘natuvchi")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages", verbose_name="Qabul qiluvchi")
    message = models.TextField(verbose_name="Xabar")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Vaqt")

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"
    
    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"


# Imtihonlar
class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exams", verbose_name="Fan")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="exams", verbose_name="Guruh")
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    date = models.DateField(verbose_name="Sana")
    test_questions = models.TextField(blank=True, null=True, verbose_name="Test savollar")  # Testlar matn shaklida saqlanadi
    max_score = models.PositiveIntegerField(default=100, verbose_name="Maksimal ball")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Imtihon"
        verbose_name_plural = "Imtihonlar"


# Imtihon natijalari
class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results", verbose_name="Imtihon")
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': UserRole.STUDENT}, verbose_name="Talaba")
    score = models.PositiveIntegerField(verbose_name="Ball")

    class Meta:
        unique_together = ('exam', 'student')
        verbose_name = "Imtihon natijasi"
        verbose_name_plural = "Imtihon natijalari"

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}: {self.score} ball"