from django import forms
from .models import Attendance, Timetable, Announcement, Exam, ExamResult


# 🔹 Yo‘qlama olish shakli
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'is_present']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'is_present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# 🔹 Dars jadvali yaratish shakli
class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['teacher', 'subject', 'group', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'day_of_week': forms.Select(choices=[
                ('Monday', 'Dushanba'),
                ('Tuesday', 'Seshanba'),
                ('Wednesday', 'Chorshanba'),
                ('Thursday', 'Payshanba'),
                ('Friday', 'Juma'),
                ('Saturday', 'Shanba'),
            ], attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }


# 🔹 E‘lon qo‘shish shakli
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['teacher', 'subject', 'title', 'content']  # 'subject' qo‘shildi
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),  # Fan tanlash uchun
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


# 🔹 Imtihon yaratish shakli
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'group', 'title', 'date', 'max_score']  # 'exam_date' emas, 'date' ishlatilgan
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# 🔹 Imtihon natijalarini kiritish shakli
class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['student', 'exam', 'score']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'exam': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }