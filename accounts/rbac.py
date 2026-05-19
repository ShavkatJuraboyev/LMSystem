from __future__ import annotations

from functools import wraps
from typing import Iterable

from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from .models import Role, RolePermission, UserRoleAssignment


ROLE_SUPERADMIN = "superadmin"
ROLE_ADMIN = "admin"
ROLE_RECTOR = "rector"
ROLE_PRORECTOR = "prorector"
ROLE_DEAN = "dean"
ROLE_DEPARTMENT_HEAD = "department_head"
ROLE_TEACHER = "teacher"
ROLE_STUDENT = "student"
ROLE_QUALITY_CONTROL = "quality_control"
ROLE_CUSTOM = "custom"


ROLE_PRIORITY = {
    ROLE_SUPERADMIN: 100,
    ROLE_ADMIN: 90,
    ROLE_RECTOR: 80,
    ROLE_PRORECTOR: 70,
    ROLE_DEAN: 60,
    ROLE_DEPARTMENT_HEAD: 50,
    ROLE_QUALITY_CONTROL: 45,
    ROLE_TEACHER: 40,
    ROLE_STUDENT: 10,
    ROLE_CUSTOM: 1,
}


DASHBOARD_TEMPLATE_MAP = {
    ROLE_SUPERADMIN: "dashboards/superadmin.html",
    ROLE_ADMIN: "dashboards/admin.html",
    ROLE_RECTOR: "dashboards/rector.html",
    ROLE_PRORECTOR: "dashboards/prorector.html",
    ROLE_DEAN: "dashboards/dean.html",
    ROLE_DEPARTMENT_HEAD: "dashboards/department_head.html",
    ROLE_TEACHER: "dashboards/teacher.html",
    ROLE_STUDENT: "dashboards/student.html",
    ROLE_QUALITY_CONTROL: "dashboards/quality.html",
    ROLE_CUSTOM: "dashboards/custom.html",
}


# Modul -> permission actionlar. Management command shu xaritadan ruxsatlarni yaratadi.
MODULE_PERMISSION_MATRIX = {
    "dashboard": {
        "name": "Dashboard",
        "actions": ["view"],
    },
    "organizations": {
        "name": "Muassasalar",
        "actions": ["view", "create", "update", "delete", "manage", "export", "audit"],
    },
    "structure": {
        "name": "Tashkiliy tuzilma",
        "actions": ["view", "create", "update", "delete", "manage", "export"],
    },
    "users": {
        "name": "Foydalanuvchilar",
        "actions": ["view", "create", "update", "delete", "manage", "export", "audit"],
    },
    "roles": {
        "name": "Rollar va ruxsatlar",
        "actions": ["view", "create", "update", "delete", "manage", "audit"],
    },
    "subjects": {
        "name": "Fanlar",
        "actions": ["view", "create", "update", "delete", "approve", "manage", "export"],
    },
    "content": {
        "name": "Kontent",
        "actions": ["view", "create", "update", "delete", "approve", "manage", "export", "audit"],
    },
    "schedule": {
        "name": "Dars jadvali",
        "actions": ["view", "create", "update", "delete", "manage", "export"],
    },
    "journal": {
        "name": "Elektron jurnal",
        "actions": ["view", "create", "update", "manage", "export", "audit"],
    },
    "attendance": {
        "name": "Davomad",
        "actions": ["view", "create", "update", "manage", "export", "audit"],
    },
    "grades": {
        "name": "Baholash",
        "actions": ["view", "create", "update", "approve", "manage", "export", "audit"],
    },
    "tests": {
        "name": "Test va topshiriqlar",
        "actions": ["view", "create", "update", "delete", "approve", "manage", "export"],
    },
    "appeals": {
        "name": "Apellyatsiya",
        "actions": ["view", "create", "update", "approve", "manage", "export"],
    },
    "quality": {
        "name": "Ta'lim sifati nazorati",
        "actions": ["view", "create", "update", "approve", "manage", "export", "audit"],
    },
    "reports": {
        "name": "Hisobotlar",
        "actions": ["view", "export", "manage"],
    },
    "documents": {
        "name": "Hujjatlar va buyruqlar",
        "actions": ["view", "create", "update", "delete", "approve", "manage", "export", "audit"],
    },
    "messages": {
        "name": "Xabar va murojaatlar",
        "actions": ["view", "create", "update", "manage", "export"],
    },
    "integrations": {
        "name": "Integratsiyalar",
        "actions": ["view", "create", "update", "delete", "manage", "audit"],
    },
    "audit": {
        "name": "Audit jurnali",
        "actions": ["view", "export", "audit"],
    },
    "settings": {
        "name": "Tizim sozlamalari",
        "actions": ["view", "update", "manage", "audit"],
    },
}


# Rol -> ruxsat kodlari. custom rolda boshlang'ich ruxsat yo'q, superadmin hammasini oladi.
ROLE_DEFAULT_PERMISSION_CODES = {
    ROLE_SUPERADMIN: ["*"],
    ROLE_ADMIN: [
        "dashboard.view",
        "structure.view", "structure.create", "structure.update", "structure.delete", "structure.manage", "structure.export",
        "users.view", "users.create", "users.update", "users.delete", "users.manage", "users.export",
        "roles.view", "roles.create", "roles.update", "roles.manage",
        "subjects.view", "subjects.create", "subjects.update", "subjects.delete", "subjects.manage", "subjects.export",
        "content.view", "content.create", "content.update", "content.delete", "content.approve", "content.manage", "content.export",
        "schedule.view", "schedule.create", "schedule.update", "schedule.delete", "schedule.manage", "schedule.export",
        "journal.view", "journal.manage", "journal.export",
        "attendance.view", "attendance.manage", "attendance.export",
        "grades.view", "grades.manage", "grades.export",
        "tests.view", "tests.manage", "tests.export",
        "reports.view", "reports.export",
        "documents.view", "documents.create", "documents.update", "documents.approve", "documents.manage", "documents.export",
        "messages.view", "messages.create", "messages.update", "messages.manage",
        "integrations.view", "integrations.update", "integrations.manage",
        "audit.view", "audit.export",
        "settings.view", "settings.update",
    ],
    ROLE_RECTOR: [
        "dashboard.view",
        "structure.view", "users.view", "subjects.view", "content.view", "schedule.view",
        "journal.view", "attendance.view", "grades.view", "tests.view",
        "quality.view", "quality.audit",
        "reports.view", "reports.export",
        "documents.view", "documents.approve", "documents.export",
        "messages.view", "messages.create", "messages.manage",
        "audit.view",
    ],
    ROLE_PRORECTOR: [
        "dashboard.view",
        "structure.view", "users.view", "subjects.view", "content.view", "schedule.view",
        "journal.view", "attendance.view", "grades.view", "tests.view",
        "quality.view", "quality.create", "quality.update", "quality.manage", "quality.export",
        "reports.view", "reports.export",
        "documents.view", "documents.create", "documents.update", "documents.approve",
        "messages.view", "messages.create", "messages.manage",
    ],
    ROLE_DEAN: [
        "dashboard.view",
        "structure.view", "users.view", "users.create", "users.update",
        "subjects.view", "content.view", "schedule.view", "schedule.create", "schedule.update",
        "journal.view", "attendance.view", "attendance.update", "attendance.manage",
        "grades.view", "grades.manage", "tests.view",
        "appeals.view", "appeals.update", "appeals.manage",
        "reports.view", "reports.export",
        "messages.view", "messages.create", "messages.update", "messages.manage",
    ],
    ROLE_DEPARTMENT_HEAD: [
        "dashboard.view",
        "structure.view", "users.view",
        "subjects.view", "subjects.update", "subjects.approve",
        "content.view", "content.create", "content.update", "content.approve", "content.manage",
        "schedule.view", "journal.view", "attendance.view",
        "grades.view", "grades.manage", "tests.view", "tests.approve", "tests.manage",
        "quality.view", "quality.update",
        "reports.view", "reports.export",
        "messages.view", "messages.create", "messages.update",
    ],
    ROLE_TEACHER: [
        "dashboard.view",
        "subjects.view",
        "content.view", "content.create", "content.update",
        "schedule.view",
        "journal.view", "journal.create", "journal.update",
        "attendance.view", "attendance.create", "attendance.update",
        "grades.view", "grades.create", "grades.update",
        "tests.view", "tests.create", "tests.update",
        "appeals.view", "appeals.update",
        "reports.view", "reports.export",
        "messages.view", "messages.create", "messages.update",
    ],
    ROLE_STUDENT: [
        "dashboard.view",
        "subjects.view", "content.view", "schedule.view",
        "attendance.view", "grades.view", "tests.view", "tests.create",
        "appeals.view", "appeals.create",
        "reports.view",
        "messages.view", "messages.create",
    ],
    ROLE_QUALITY_CONTROL: [
        "dashboard.view",
        "structure.view", "users.view", "subjects.view", "content.view", "content.audit",
        "schedule.view", "journal.view", "attendance.view", "grades.view", "grades.audit", "tests.view",
        "quality.view", "quality.create", "quality.update", "quality.approve", "quality.manage", "quality.export", "quality.audit",
        "reports.view", "reports.export",
        "messages.view", "messages.create", "messages.update",
        "audit.view",
    ],
    ROLE_CUSTOM: [],
}


ROLE_LABELS = {
    ROLE_SUPERADMIN: "Superadmin",
    ROLE_ADMIN: "Admin",
    ROLE_RECTOR: "Rektor",
    ROLE_PRORECTOR: "Prorektor",
    ROLE_DEAN: "Dekan",
    ROLE_DEPARTMENT_HEAD: "Kafedra mudiri",
    ROLE_TEACHER: "O'qituvchi",
    ROLE_STUDENT: "Talaba",
    ROLE_QUALITY_CONTROL: "Ta'lim sifati nazorati",
    ROLE_CUSTOM: "Maxsus rol",
}


def get_active_assignments(user):
    if not user or not user.is_authenticated:
        return UserRoleAssignment.objects.none()

    now = timezone.now()

    return (
        UserRoleAssignment.objects
        .select_related("role", "organization", "faculty", "department", "group", "subject")
        .filter(user=user, is_active=True, role__is_active=True)
        .filter(
            # muddatsiz yoki hali tugamagan
            # starts_at bo'sh bo'lsa ham faol hisoblanadi
        )
    )


def get_user_assignments(user):
    if not user or not user.is_authenticated:
        return []

    now = timezone.now()

    qs = (
        user.role_assignments
        .select_related("role", "organization", "faculty", "department", "group", "subject")
        .filter(is_active=True, role__is_active=True)
    )

    qs = qs.filter(starts_at__isnull=True) | qs.filter(starts_at__lte=now)
    qs = qs.filter(ends_at__isnull=True) | qs.filter(ends_at__gte=now)

    return list(qs.distinct())


def get_user_role_codes(user) -> set[str]:
    if not user or not user.is_authenticated:
        return set()

    if getattr(user, "is_superuser", False):
        return {ROLE_SUPERADMIN}

    return {item.role.role_type for item in get_user_assignments(user)}


def get_primary_assignment(user):
    assignments = get_user_assignments(user)
    if not assignments:
        return None

    return sorted(
        assignments,
        key=lambda item: ROLE_PRIORITY.get(item.role.role_type, 0),
        reverse=True,
    )[0]


def get_primary_role_code(user) -> str | None:
    if getattr(user, "is_superuser", False):
        return ROLE_SUPERADMIN

    assignment = get_primary_assignment(user)
    return assignment.role.role_type if assignment else None


def has_role(user, roles: str | Iterable[str]) -> bool:
    if isinstance(roles, str):
        roles = [roles]

    if getattr(user, "is_superuser", False):
        return True

    return bool(get_user_role_codes(user).intersection(set(roles)))


def get_permission_codes(user) -> set[str]:
    if not user or not user.is_authenticated:
        return set()

    if getattr(user, "is_superuser", False):
        return {"*"}

    role_ids = [item.role_id for item in get_user_assignments(user)]
    if not role_ids:
        return set()

    return set(
        RolePermission.objects
        .filter(role_id__in=role_ids, permission__module__is_active=True)
        .select_related("permission")
        .values_list("permission__code", flat=True)
    )


def has_permission(user, permission_code: str) -> bool:
    if getattr(user, "is_superuser", False):
        return True

    codes = get_permission_codes(user)
    return "*" in codes or permission_code in codes


def has_any_permission(user, permission_codes: Iterable[str]) -> bool:
    if getattr(user, "is_superuser", False):
        return True

    codes = get_permission_codes(user)
    return "*" in codes or bool(set(permission_codes).intersection(codes))


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if has_role(request.user, roles):
                return view_func(request, *args, **kwargs)

            messages.error(request, "Ushbu sahifaga kirish uchun sizda rol yetarli emas.")
            return redirect("dashboard")

        return wrapped

    return decorator


def permission_required(*permission_codes):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if has_any_permission(request.user, permission_codes):
                return view_func(request, *args, **kwargs)

            messages.error(request, "Ushbu amal uchun sizda ruxsat mavjud emas.")
            return redirect("dashboard")

        return wrapped

    return decorator


def get_user_scope(user):
    """
    Bir foydalanuvchida bir nechta rol bo'lsa, barcha scope lar birlashadi.
    Masalan: bir user Dean + Teacher bo'lishi mumkin.
    """
    scope = {
        "organization_ids": set(),
        "faculty_ids": set(),
        "department_ids": set(),
        "group_ids": set(),
        "subject_ids": set(),
    }

    if not user or not user.is_authenticated:
        return scope

    if getattr(user, "organization_id", None):
        scope["organization_ids"].add(user.organization_id)

    for item in get_user_assignments(user):
        if item.organization_id:
            scope["organization_ids"].add(item.organization_id)
        if item.faculty_id:
            scope["faculty_ids"].add(item.faculty_id)
        if item.department_id:
            scope["department_ids"].add(item.department_id)
        if item.group_id:
            scope["group_ids"].add(item.group_id)
        if item.subject_id:
            scope["subject_ids"].add(item.subject_id)

    return scope


def filter_queryset_by_scope(user, queryset, organization_field="organization_id", faculty_field="faculty_id",
                             department_field="department_id", group_field="group_id", subject_field="subject_id"):
    """
    ListView/API querysetlarni rol scope bo'yicha cheklash uchun.
    Superadmin hammasini ko'radi.
    Admin organization bo'yicha, Dean faculty bo'yicha, Department head department bo'yicha,
    Teacher subject/group bo'yicha, Student faqat o'z ma'lumotlari bo'yicha ishlatiladi.
    """
    if getattr(user, "is_superuser", False) or has_role(user, ROLE_SUPERADMIN):
        return queryset

    from django.db.models import Q

    role_codes = get_user_role_codes(user)
    scope = get_user_scope(user)
    q = Q()

    if ROLE_ADMIN in role_codes or ROLE_RECTOR in role_codes or ROLE_PRORECTOR in role_codes:
        if scope["organization_ids"]:
            q |= Q(**{f"{organization_field}__in": scope["organization_ids"]})

    if ROLE_DEAN in role_codes and scope["faculty_ids"]:
        q |= Q(**{f"{faculty_field}__in": scope["faculty_ids"]})

    if ROLE_DEPARTMENT_HEAD in role_codes and scope["department_ids"]:
        q |= Q(**{f"{department_field}__in": scope["department_ids"]})

    if ROLE_TEACHER in role_codes:
        if scope["group_ids"]:
            q |= Q(**{f"{group_field}__in": scope["group_ids"]})
        if scope["subject_ids"]:
            q |= Q(**{f"{subject_field}__in": scope["subject_ids"]})

    if not q:
        return queryset.none()

    return queryset.filter(q).distinct()
