from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q

from core.models import BaseModel, EducationForm, EducationLevel, SemesterType, UserStatus


class Organization(BaseModel):
    name = models.CharField("Muassasa nomi", max_length=255)
    short_name = models.CharField("Qisqa nomi", max_length=100, blank=True)
    code = models.CharField("Muassasa kodi", max_length=50, unique=True)
    tin = models.CharField("STIR", max_length=20, blank=True)
    address = models.TextField("Manzil", blank=True)
    phone = models.CharField("Telefon", max_length=30, blank=True)
    email = models.EmailField("E-mail", blank=True)
    website = models.URLField("Veb-sayt", blank=True)
    rector_full_name = models.CharField("Rektor F.I.Sh.", max_length=255, blank=True)
    status = models.CharField("Holat", max_length=20, choices=UserStatus.choices, default=UserStatus.ACTIVE)

    class Meta:
        verbose_name = "Muassasa"
        verbose_name_plural = "Muassasalar"
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.short_name or self.name


class Faculty(BaseModel):
    organization = models.ForeignKey(Organization, verbose_name="Muassasa", on_delete=models.CASCADE, related_name="faculties")
    name = models.CharField("Fakultet nomi", max_length=255)
    code = models.CharField("Fakultet kodi", max_length=50)
    dean = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Dekan", null=True, blank=True, on_delete=models.SET_NULL, related_name="managed_faculties")
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Fakultet"
        verbose_name_plural = "Fakultetlar"
        unique_together = ("organization", "code")
        indexes = [models.Index(fields=["organization", "is_active"])]

    def __str__(self):
        return self.name


class Department(BaseModel):
    organization = models.ForeignKey(Organization, verbose_name="Muassasa", on_delete=models.CASCADE, related_name="departments")
    faculty = models.ForeignKey(Faculty, verbose_name="Fakultet", on_delete=models.CASCADE, related_name="departments")
    name = models.CharField("Kafedra nomi", max_length=255)
    code = models.CharField("Kafedra kodi", max_length=50)
    head = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Kafedra mudiri", null=True, blank=True, on_delete=models.SET_NULL, related_name="managed_departments")
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Kafedra"
        verbose_name_plural = "Kafedralar"
        unique_together = ("faculty", "code")
        indexes = [models.Index(fields=["organization", "faculty", "is_active"])]

    def __str__(self):
        return self.name


class Specialty(BaseModel):
    organization = models.ForeignKey(Organization, verbose_name="Muassasa", on_delete=models.CASCADE, related_name="specialties")
    faculty = models.ForeignKey(Faculty, verbose_name="Fakultet", on_delete=models.CASCADE, related_name="specialties")
    department = models.ForeignKey(Department, verbose_name="Kafedra", null=True, blank=True, on_delete=models.SET_NULL, related_name="specialties")
    code = models.CharField("Yo'nalish kodi", max_length=50)
    name = models.CharField("Yo'nalish nomi", max_length=255)
    education_level = models.CharField("Ta'lim bosqichi", max_length=30, choices=EducationLevel.choices)
    education_form = models.CharField("Ta'lim shakli", max_length=30, choices=EducationForm.choices)
    duration_years = models.PositiveSmallIntegerField("O'qish muddati", default=4)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Ta'lim yo'nalishi"
        verbose_name_plural = "Ta'lim yo'nalishlari"
        unique_together = ("organization", "code")
        indexes = [models.Index(fields=["faculty", "education_level", "education_form"])]


class AcademicYear(BaseModel):
    organization = models.ForeignKey(
        Organization,
        verbose_name="Muassasa",
        on_delete=models.CASCADE,
        related_name="academic_years"
    )
    name = models.CharField(
        "O'quv yili",
        max_length=20,
        help_text="Masalan: 2026/2027"
    )
    start_date = models.DateField("Boshlanish sanasi")
    end_date = models.DateField("Tugash sanasi")
    is_current = models.BooleanField("Joriy o'quv yilimi", default=False)

    class Meta:
        verbose_name = "O'quv yili"
        verbose_name_plural = "O'quv yillari"
        unique_together = ("organization", "name")
        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gt=models.F("start_date")),
                name="academic_year_end_after_start"
            ),
        ]


class Semester(BaseModel):
    organization = models.ForeignKey(Organization, verbose_name="Muassasa", on_delete=models.CASCADE, related_name="semesters")
    academic_year = models.ForeignKey(AcademicYear, verbose_name="O'quv yili", on_delete=models.CASCADE, related_name="semesters")
    name = models.CharField("Semestr nomi", max_length=100)
    semester_type = models.CharField("Semestr turi", max_length=20, choices=SemesterType.choices)
    number = models.PositiveSmallIntegerField("Semestr raqami")
    start_date = models.DateField("Boshlanish sanasi")
    end_date = models.DateField("Tugash sanasi")
    is_current = models.BooleanField("Joriy semestrmi", default=False)

    class Meta:
        verbose_name = "Semestr"
        verbose_name_plural = "Semestrlar"
        unique_together = ("academic_year", "number")
        indexes = [models.Index(fields=["organization", "is_current"])]


class Group(BaseModel):
    organization = models.ForeignKey(Organization, verbose_name="Muassasa", on_delete=models.CASCADE, related_name="groups")
    faculty = models.ForeignKey(Faculty, verbose_name="Fakultet", on_delete=models.PROTECT, related_name="groups")
    department = models.ForeignKey(Department, verbose_name="Kafedra", null=True, blank=True, on_delete=models.SET_NULL, related_name="groups")
    specialty = models.ForeignKey(Specialty, verbose_name="Yo'nalish", on_delete=models.PROTECT, related_name="groups")
    academic_year = models.ForeignKey(AcademicYear, verbose_name="Qabul o'quv yili", on_delete=models.PROTECT, related_name="groups")
    name = models.CharField("Guruh nomi", max_length=100)
    course = models.PositiveSmallIntegerField("Kurs")
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Tyutor/Kurator", null=True, blank=True, on_delete=models.SET_NULL, related_name="curator_groups")
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        unique_together = ("organization", "name")
        indexes = [
            models.Index(fields=["faculty", "course"]),
            models.Index(fields=["specialty", "course"]),
        ]

    def __str__(self):
        return self.name


class Auditorium(BaseModel):
    organization = models.ForeignKey(Organization, verbose_name="Muassasa", on_delete=models.CASCADE, related_name="auditoriums")
    building = models.CharField("Bino", max_length=100, blank=True)
    name = models.CharField("Auditoriya", max_length=100)
    capacity = models.PositiveIntegerField("Sig'im", default=0)
    has_projector = models.BooleanField("Proyektor bormi", default=False)
    has_computers = models.BooleanField("Kompyuterlar bormi", default=False)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Auditoriya"
        verbose_name_plural = "Auditoriyalar"
        unique_together = ("organization", "building", "name")
