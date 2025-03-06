from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import FileExtensionValidator


# 1. Foydalanuvchi modelini kengaytirish
class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Talaba'),
        ('teacher', 'O‘qituvchi'),
        ('department_head', 'Kafedra mudiri'),
        ('dean', 'Dekan'),
        ('admin', 'Administrator'),
        ('super_admin', 'Super Admin'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)
 
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


# 2. Kafedra modeli
class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    head = models.OneToOneField(User, on_delete=models.SET_NULL, limit_choices_to={'user_type': 'department_head'},  null=True, blank=True, related_name="managed_department")

    def __str__(self):
        return self.name


# 3. Dekanat modeli (Dekan va unga bog‘liq kafedralar)
class DeanOffice(models.Model):
    dean = models.OneToOneField(User, on_delete=models.SET_NULL, limit_choices_to={'user_type': 'dean'}, null=True, blank=True, related_name="dean_office")
    departments = models.ManyToManyField(Department, related_name="dean_offices")

    def __str__(self):
        return f"Dekan: {self.dean.username}" if self.dean else "Bo‘sh Dekanat"


# 4. Kurslar modeli
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.name


# 5. Fan modeli
class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
    teachers = models.ManyToManyField(User, limit_choices_to={'user_type': 'teacher'}, related_name="subjects")

    def __str__(self):
        return f"{self.name} ({self.course.name})"


# 6. O‘qituvchilarni kafedraga bog‘lash
class TeacherDepartment(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'},
                                   related_name="teacher_department")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="teachers")

    def __str__(self):
        return f"{self.teacher.username} - {self.department.name}"


# 7. Guruh modeli
class Group(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    students = models.ManyToManyField(User, limit_choices_to={'user_type': 'student'}, related_name="groups")
    teachers = models.ManyToManyField(User, limit_choices_to={'user_type': 'teacher'}, related_name="teacher_groups")

    def __str__(self):
        return self.name


# 8. Talabaning kursga bog‘lanishi
class StudentCourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"


# 9. Dars jadvallari
class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="schedules")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="schedules")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'})
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.subject.name} - {self.group.name} ({self.date_time})"


# 10. Topshiriqlar (vazifalar)
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="assignments")
    due_date = models.DateTimeField()
    file = models.FileField(upload_to='assignments/', blank=True, null=True,
                            validators=[FileExtensionValidator(['pdf', 'docx', 'pptx'])])

    def __str__(self):
        return f"{self.title} ({self.subject.name})"


# 11. Talabalarning topshiriqlari
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', validators=[FileExtensionValidator(['pdf', 'docx', 'pptx'])])
    is_graded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


# 12. Baholash tizimi
class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name="grade")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'})
    score = models.PositiveIntegerField()
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.submission.student.username} - {self.score}"


# 13. Dars materiallari
class CourseMaterial(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='course_materials/', validators=[FileExtensionValidator(['pdf', 'docx', 'pptx', 'mp4'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 14. Talabalar davomatini saqlash (yo‘qlama tizimi)
class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)  # True - qatnashgan, False - qatnashmagan

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} ({'Qatnashdi' if self.is_present else 'Qatnashmadi'})"


# 15. O‘qituvchi va talaba xabar almashish tizimi
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.message[:30]}"


# 16. O‘qituvchilar uchun e‘lonlar tizimi
class Announcement(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.teacher.username})"


# 17. Imtihonlar tizimi
class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exams")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField(max_length=255)
    date = models.DateField()
    max_score = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.date})"


# 18. Imtihon natijalari
class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    score = models.PositiveIntegerField()

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}: {self.score} ball"
