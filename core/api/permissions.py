from rest_framework.permissions import BasePermission, SAFE_METHODS

from .roles import (
    MANAGEMENT_ROLES,
    ROLE_ADMIN,
    ROLE_DEAN,
    ROLE_DEPARTMENT_HEAD,
    ROLE_PRORECTOR,
    ROLE_QUALITY_CONTROL,
    ROLE_RECTOR,
    ROLE_STUDENT,
    ROLE_SUPERADMIN,
    ROLE_TEACHER,
)


def user_role_codes(user):
    if not user or not user.is_authenticated:
        return set()

    if getattr(user, "is_superuser", False):
        return {ROLE_SUPERADMIN}

    try:
        return set(
            user.role_assignments.filter(
                is_active=True,
                role__is_active=True,
            ).values_list("role__role_type", flat=True)
        )
    except Exception:
        return set()


def has_any_role(user, roles):
    return bool(user_role_codes(user).intersection(set(roles)))


def has_all_roles(user, roles):
    return set(roles).issubset(user_role_codes(user))


def get_assignment_scopes(user):
    scopes = {
        "organizations": set(),
        "faculties": set(),
        "departments": set(),
        "groups": set(),
        "subjects": set(),
    }

    if not user or not user.is_authenticated:
        return scopes

    try:
        assignments = user.role_assignments.filter(
            is_active=True,
            role__is_active=True,
        ).select_related(
            "organization",
            "faculty",
            "department",
            "group",
            "subject",
            "role",
        )

        for item in assignments:
            if item.organization_id:
                scopes["organizations"].add(item.organization_id)

            if item.faculty_id:
                scopes["faculties"].add(item.faculty_id)

            if item.department_id:
                scopes["departments"].add(item.department_id)

            if item.group_id:
                scopes["groups"].add(item.group_id)

            if item.subject_id:
                scopes["subjects"].add(item.subject_id)

    except Exception:
        pass

    return scopes


def get_user_organization_id(user):
    return getattr(user, "organization_id", None)


def is_same_organization(user, obj, organization_attr="organization_id"):
    if getattr(user, "is_superuser", False):
        return True

    user_org_id = get_user_organization_id(user)
    if not user_org_id:
        return False

    obj_org_id = getattr(obj, organization_attr, None)

    if not obj_org_id and hasattr(obj, "organization"):
        obj_org_id = getattr(obj.organization, "id", None)

    return str(user_org_id) == str(obj_org_id)


# Eski kodlar ishlashi uchun alias
def same_organization(user, obj, organization_attr="organization_id"):
    return is_same_organization(user, obj, organization_attr)


class IsAuthenticatedActive(BasePermission):
    message = "Tizimga kirgan va faol foydalanuvchi bo'lishingiz kerak."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "is_active", False)
            and getattr(user, "status", "active") == "active"
        )


# Eski views.py fayllar ishlashi uchun alias
class IsAuthenticatedAndActive(IsAuthenticatedActive):
    pass


class HasAnyRole(BasePermission):
    """
    View ichida:
        required_roles = ["admin", "superadmin"]
    """

    message = "Ushbu amal uchun sizda yetarli rol mavjud emas."

    def has_permission(self, request, view):
        required_roles = getattr(view, "required_roles", [])

        if not required_roles:
            return request.user and request.user.is_authenticated

        return has_any_role(request.user, required_roles)


class IsSuperAdmin(BasePermission):
    message = "Faqat superadmin uchun ruxsat berilgan."

    def has_permission(self, request, view):
        return request.user.is_authenticated and has_any_role(
            request.user,
            [ROLE_SUPERADMIN],
        )


class IsAdminOrSuperAdmin(BasePermission):
    message = "Faqat admin yoki superadmin uchun ruxsat."

    def has_permission(self, request, view):
        return request.user.is_authenticated and has_any_role(
            request.user,
            [ROLE_SUPERADMIN, ROLE_ADMIN],
        )


class IsManagementRole(BasePermission):
    message = "Faqat rahbariyat yoki mas'ul rollar uchun ruxsat."

    def has_permission(self, request, view):
        return request.user.is_authenticated and has_any_role(
            request.user,
            MANAGEMENT_ROLES,
        )


class RoleActionPermission(BasePermission):
    """
    ViewSet ichida action bo'yicha ruxsat:

    role_action_permissions = {
        "list": ["admin", "rector"],
        "retrieve": ["admin", "rector", "teacher"],
        "create": ["admin"],
        "update": ["admin"],
        "partial_update": ["admin"],
        "destroy": ["superadmin"],
    }
    """

    message = "Ushbu action uchun ruxsat yo'q."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, "is_superuser", False):
            return True

        action = getattr(view, "action", None)
        rules = getattr(view, "role_action_permissions", {})

        if not rules:
            return True

        required = (
            rules.get(action)
            or rules.get(request.method.lower())
            or rules.get("*")
        )

        if required is None:
            return False

        return has_any_role(request.user, required)


class ReadOnlyForManagementWriteForAdmin(BasePermission):
    """
    Rahbariyat ko'radi, admin/superadmin yozadi.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return has_any_role(
                request.user,
                MANAGEMENT_ROLES | {ROLE_TEACHER},
            )

        return has_any_role(
            request.user,
            [ROLE_SUPERADMIN, ROLE_ADMIN],
        )


class TeacherSubjectObjectPermission(BasePermission):
    """
    O'qituvchi faqat o'z SubjectGroup/Topic/Content/Assignment/Test/Jurnal obyektlariga ishlaydi.
    """

    message = "Faqat o'zingizga biriktirilgan fan/guruh obyektiga ruxsat bor."

    def has_permission(self, request, view):
        return request.user.is_authenticated and has_any_role(
            request.user,
            [
                ROLE_SUPERADMIN,
                ROLE_ADMIN,
                ROLE_TEACHER,
                ROLE_DEPARTMENT_HEAD,
                ROLE_DEAN,
            ],
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if has_any_role(user, [ROLE_SUPERADMIN, ROLE_ADMIN]):
            return True

        roles = user_role_codes(user)
        scopes = get_assignment_scopes(user)

        subject_group = getattr(obj, "subject_group", None)

        if subject_group is None and hasattr(obj, "topic"):
            subject_group = getattr(obj.topic, "subject_group", None)

        if subject_group is None and hasattr(obj, "assignment"):
            subject_group = getattr(obj.assignment, "subject_group", None)

        if subject_group is None and hasattr(obj, "test"):
            subject_group = getattr(obj.test, "subject_group", None)

        if subject_group is None and obj.__class__.__name__ == "SubjectGroup":
            subject_group = obj

        if not subject_group:
            return False

        if ROLE_TEACHER in roles:
            if getattr(subject_group, "main_teacher_id", None) == user.id:
                return True

            try:
                if subject_group.assistant_teachers.filter(id=user.id).exists():
                    return True
            except Exception:
                pass

            if getattr(subject_group, "subject_id", None) in scopes["subjects"]:
                return True

            if getattr(subject_group, "group_id", None) in scopes["groups"]:
                return True

        if ROLE_DEPARTMENT_HEAD in roles:
            subject = getattr(subject_group, "subject", None)
            return bool(
                subject
                and getattr(subject, "department_id", None) in scopes["departments"]
            )

        if ROLE_DEAN in roles:
            group = getattr(subject_group, "group", None)
            return bool(
                group
                and getattr(group, "faculty_id", None) in scopes["faculties"]
            )

        return False


# Eski views.py ishlashi uchun alias
class TeacherOwnSubjectPermission(TeacherSubjectObjectPermission):
    pass


class StudentOwnObjectPermission(BasePermission):
    """
    Talaba faqat o'ziga tegishli grade, attendance, submission, attempt, appeal'ni ko'radi.
    """

    message = "Talaba faqat o'z ma'lumotlari bilan ishlashi mumkin."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if has_any_role(user, MANAGEMENT_ROLES | {ROLE_TEACHER}):
            return True

        if not has_any_role(user, [ROLE_STUDENT]):
            return False

        student_profile = getattr(user, "student_profile", None)
        if not student_profile:
            return False

        student = getattr(obj, "student", None)

        if student:
            return str(student.id) == str(student_profile.id)

        if obj.__class__.__name__ == "StudentProfile":
            return str(obj.id) == str(student_profile.id)

        attempt = getattr(obj, "attempt", None)

        if attempt and getattr(attempt, "student_id", None):
            return str(attempt.student_id) == str(student_profile.id)

        return False


# Eski views.py ishlashi uchun alias
class StudentOwnDataPermission(StudentOwnObjectPermission):
    pass


class QualityControlPermission(BasePermission):
    message = "Ta'lim sifati nazorati huquqi kerak."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return has_any_role(request.user, MANAGEMENT_ROLES)

        return has_any_role(
            request.user,
            [ROLE_SUPERADMIN, ROLE_ADMIN, ROLE_QUALITY_CONTROL],
        )


class DocumentWorkflowPermission(BasePermission):
    message = "Hujjatlar moduli uchun ruxsat yo'q."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return has_any_role(
                request.user,
                [
                    ROLE_SUPERADMIN,
                    ROLE_ADMIN,
                    ROLE_RECTOR,
                    ROLE_PRORECTOR,
                    ROLE_DEAN,
                    ROLE_DEPARTMENT_HEAD,
                ],
            )

        return has_any_role(
            request.user,
            [
                ROLE_SUPERADMIN,
                ROLE_ADMIN,
                ROLE_RECTOR,
                ROLE_PRORECTOR,
                ROLE_DEAN,
            ],
        )


class DenyDeleteExceptSuperAdmin(BasePermission):
    message = "O'chirish faqat superadmin uchun."

    def has_permission(self, request, view):
        if request.method.lower() == "delete":
            return has_any_role(request.user, [ROLE_SUPERADMIN])

        return True