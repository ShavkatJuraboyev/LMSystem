from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from core.models import BaseModel, Gender, UserStatus


class User(AbstractUser):
    """
    LMS tizimidagi barcha foydalanuvchilar:
    superadmin, admin, rektor, prorektor, dekan, kafedra mudiri,
    o'qituvchi, talaba va ta'lim sifati nazorati xodimi.
    """
    import uuid

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "structure.Organization",
        verbose_name="Muassasa",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="users",
    )
    middle_name = models.CharField("Otasining ismi", max_length=150, blank=True)
    phone = models.CharField("Telefon", max_length=30, blank=True, db_index=True)
    passport_pinfl = models.CharField("JSHSHIR/PINFL", max_length=14, blank=True, db_index=True)
    birth_date = models.DateField("Tug'ilgan sana", null=True, blank=True)
    gender = models.CharField("Jinsi", max_length=20, choices=Gender.choices, blank=True)
    avatar = models.ImageField("Rasm", upload_to="users/avatars/%Y/%m/", null=True, blank=True)

    status = models.CharField("Holat", max_length=20, choices=UserStatus.choices, default=UserStatus.ACTIVE, db_index=True)
    two_factor_enabled = models.BooleanField("2FA yoqilganmi", default=False)
    last_password_change = models.DateTimeField("Parol oxirgi o'zgartirilgan vaqt", null=True, blank=True)
    last_activity_at = models.DateTimeField("Oxirgi faollik", null=True, blank=True)
    failed_login_attempts = models.PositiveSmallIntegerField("Muvaffaqiyatsiz login urinishlari", default=0)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["passport_pinfl"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "passport_pinfl"],
                condition=Q(passport_pinfl__gt=""),
                name="unique_user_pinfl_per_organization",
            ),
        ]

    @property
    def full_name(self):
        return " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))


class Module(models.Model):
    code = models.CharField("Modul kodi", max_length=80, unique=True)
    name = models.CharField("Modul nomi", max_length=150)
    description = models.TextField("Izoh", blank=True)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Modul"
        verbose_name_plural = "Modullar"

    def __str__(self):
        return self.name


class Permission(models.Model):
    class Action(models.TextChoices):
        VIEW = "view", "Ko'rish"
        CREATE = "create", "Yaratish"
        UPDATE = "update", "Tahrirlash"
        DELETE = "delete", "O'chirish"
        APPROVE = "approve", "Tasdiqlash"
        EXPORT = "export", "Eksport"
        IMPORT = "import", "Import"
        AUDIT = "audit", "Audit"
        MANAGE = "manage", "Boshqarish"

    module = models.ForeignKey(Module, verbose_name="Modul", on_delete=models.CASCADE, related_name="permissions")
    action = models.CharField("Amal", max_length=30, choices=Action.choices)
    code = models.CharField("Ruxsat kodi", max_length=120, unique=True)
    name = models.CharField("Ruxsat nomi", max_length=150)
    description = models.TextField("Izoh", blank=True)

    class Meta:
        verbose_name = "Ruxsat"
        verbose_name_plural = "Ruxsatlar"
        unique_together = ("module", "action")

    def __str__(self):
        return self.code


class Role(BaseModel):
    class RoleType(models.TextChoices):
        SUPERADMIN = "superadmin", "Superadmin"
        ADMIN = "admin", "Admin"
        RECTOR = "rector", "Rektor"
        PRORECTOR = "prorector", "Prorektor"
        DEAN = "dean", "Dekan"
        DEPARTMENT_HEAD = "department_head", "Kafedra mudiri"
        TEACHER = "teacher", "O'qituvchi"
        STUDENT = "student", "Talaba"
        QUALITY_CONTROL = "quality_control", "Ta'lim sifati nazorati"
        CUSTOM = "custom", "Maxsus rol"

    organization = models.ForeignKey(
        "structure.Organization",
        verbose_name="Muassasa",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="roles",
        help_text="Bo'sh bo'lsa, global rol hisoblanadi.",
    )
    name = models.CharField("Rol nomi", max_length=150)
    code = models.CharField("Rol kodi", max_length=80)
    role_type = models.CharField("Rol turi", max_length=50, choices=RoleType.choices, default=RoleType.CUSTOM)
    description = models.TextField("Izoh", blank=True)
    is_system = models.BooleanField("Tizim rolimi", default=False)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Rollar"
        constraints = [
            models.UniqueConstraint(fields=["organization", "code"], name="unique_role_code_per_org"),
        ]
        indexes = [
            models.Index(fields=["organization", "role_type"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, verbose_name="Rol", on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(Permission, verbose_name="Ruxsat", on_delete=models.CASCADE, related_name="role_permissions")
    conditions = models.JSONField("Qo'shimcha shartlar", default=dict, blank=True)
    created_at = models.DateTimeField("Yaratilgan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Rol ruxsati"
        verbose_name_plural = "Rol ruxsatlari"
        unique_together = ("role", "permission")


class UserRoleAssignment(BaseModel):
    """
    Scope-based role assignment:
    - Dekan faqat faculty bo'yicha
    - Kafedra mudiri faqat department bo'yicha
    - O'qituvchi faqat subject/group bo'yicha
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", on_delete=models.CASCADE, related_name="role_assignments")
    role = models.ForeignKey(Role, verbose_name="Rol", on_delete=models.PROTECT, related_name="user_assignments")

    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", null=True, blank=True, on_delete=models.CASCADE)
    faculty = models.ForeignKey("structure.Faculty", verbose_name="Fakultet", null=True, blank=True, on_delete=models.CASCADE)
    department = models.ForeignKey("structure.Department", verbose_name="Kafedra", null=True, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey("structure.Group", verbose_name="Guruh", null=True, blank=True, on_delete=models.CASCADE)
    subject = models.ForeignKey("academics.Subject", verbose_name="Fan", null=True, blank=True, on_delete=models.CASCADE)

    starts_at = models.DateTimeField("Boshlanish vaqti", null=True, blank=True)
    ends_at = models.DateTimeField("Tugash vaqti", null=True, blank=True)
    is_active = models.BooleanField("Faolmi", default=True)

    class Meta:
        verbose_name = "Foydalanuvchi roli"
        verbose_name_plural = "Foydalanuvchi rollari"
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["role", "is_active"]),
            models.Index(fields=["organization", "faculty", "department"]),
        ]


class EmployeeProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", on_delete=models.CASCADE, related_name="employee_profile")
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="employees")
    faculty = models.ForeignKey("structure.Faculty", verbose_name="Fakultet", null=True, blank=True, on_delete=models.SET_NULL, related_name="employees")
    department = models.ForeignKey("structure.Department", verbose_name="Kafedra", null=True, blank=True, on_delete=models.SET_NULL, related_name="employees")
    employee_id = models.CharField("Xodim ID", max_length=80, blank=True)
    position = models.CharField("Lavozim", max_length=150, blank=True)
    academic_degree = models.CharField("Ilmiy daraja", max_length=150, blank=True)
    academic_title = models.CharField("Ilmiy unvon", max_length=150, blank=True)
    hire_date = models.DateField("Ishga qabul qilingan sana", null=True, blank=True)
    is_teacher = models.BooleanField("O'qituvchimi", default=False)

    class Meta:
        verbose_name = "Xodim profili"
        verbose_name_plural = "Xodim profillari"
        indexes = [models.Index(fields=["organization", "faculty", "department"])]


class StudentProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Foydalanuvchi", on_delete=models.CASCADE, related_name="student_profile")
    organization = models.ForeignKey("structure.Organization", verbose_name="Muassasa", on_delete=models.CASCADE, related_name="students")
    faculty = models.ForeignKey("structure.Faculty", verbose_name="Fakultet", on_delete=models.PROTECT, related_name="students")
    department = models.ForeignKey("structure.Department", verbose_name="Kafedra", null=True, blank=True, on_delete=models.SET_NULL, related_name="students")
    specialty = models.ForeignKey("structure.Specialty", verbose_name="Yo'nalish", on_delete=models.PROTECT, related_name="students")
    group = models.ForeignKey("structure.Group", verbose_name="Guruh", on_delete=models.PROTECT, related_name="students")
    student_id = models.CharField("Talaba ID", max_length=80)
    education_form = models.CharField("Ta'lim shakli", max_length=30)
    education_level = models.CharField("Ta'lim bosqichi", max_length=30)
    course = models.PositiveSmallIntegerField("Kurs")
    admission_year = models.PositiveSmallIntegerField("Qabul yili")
    gpa = models.DecimalField("GPA", max_digits=4, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Talaba profili"
        verbose_name_plural = "Talaba profillari"
        unique_together = ("organization", "student_id")
        indexes = [
            models.Index(fields=["organization", "faculty", "group"]),
            models.Index(fields=["student_id"]),
        ]
