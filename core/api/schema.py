from copy import deepcopy

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

from .roles import ROLE_LABELS


ROLE_PATH_PREFIXES = {
    "superadmin": ["/api/v1/"],

    "admin": ["/api/v1/"],

    "rector": [
        "/api/v1/structure/",
        "/api/v1/academics/",
        "/api/v1/journal/",
        "/api/v1/assessment/",
        "/api/v1/tasks/",
        "/api/v1/communication/",
        "/api/v1/documents/",
        "/api/v1/quality/",
        "/api/v1/analytics/",
        "/api/v1/audit/audit-logs/",
    ],

    "prorector": [
        "/api/v1/structure/",
        "/api/v1/academics/",
        "/api/v1/journal/",
        "/api/v1/assessment/",
        "/api/v1/tasks/",
        "/api/v1/communication/",
        "/api/v1/documents/",
        "/api/v1/quality/",
        "/api/v1/analytics/",
    ],

    "dean": [
        "/api/v1/structure/groups/",
        "/api/v1/accounts/students/",
        "/api/v1/accounts/employees/",
        "/api/v1/academics/",
        "/api/v1/journal/",
        "/api/v1/assessment/",
        "/api/v1/tasks/",
        "/api/v1/communication/",
        "/api/v1/documents/",
        "/api/v1/quality/",
        "/api/v1/analytics/",
    ],

    "department_head": [
        "/api/v1/accounts/employees/",
        "/api/v1/academics/",
        "/api/v1/journal/",
        "/api/v1/assessment/",
        "/api/v1/tasks/",
        "/api/v1/communication/",
        "/api/v1/quality/",
        "/api/v1/analytics/",
    ],

    "teacher": [
        "/api/v1/accounts/me/",
        "/api/v1/accounts/students/",
        "/api/v1/academics/subject-groups/",
        "/api/v1/academics/topics/",
        "/api/v1/academics/contents/",
        "/api/v1/journal/schedules/",
        "/api/v1/journal/lesson-sessions/",
        "/api/v1/journal/attendances/",
        "/api/v1/assessment/grades/",
        "/api/v1/tasks/",
        "/api/v1/communication/",
    ],

    "student": [
        "/api/v1/accounts/me/",
        "/api/v1/academics/subject-groups/",
        "/api/v1/academics/topics/",
        "/api/v1/academics/contents/",
        "/api/v1/journal/schedules/",
        "/api/v1/journal/attendances/",
        "/api/v1/assessment/grades/",
        "/api/v1/assessment/appeals/",
        "/api/v1/tasks/assignments/",
        "/api/v1/tasks/submissions/",
        "/api/v1/tasks/tests/",
        "/api/v1/tasks/test-attempts/",
        "/api/v1/tasks/student-answers/",
        "/api/v1/communication/",
    ],

    "quality_control": [
        "/api/v1/structure/",
        "/api/v1/academics/",
        "/api/v1/journal/",
        "/api/v1/assessment/",
        "/api/v1/tasks/",
        "/api/v1/quality/",
        "/api/v1/analytics/",
    ],
}


def path_allowed(path, role):
    """
    Berilgan path tanlangan rolga tegishlimi yoki yo‘qmi tekshiradi.
    Masalan:
        /api/v1/accounts/me/ -> student uchun bor
        /api/v1/audit/audit-logs/ -> faqat yuqori rollar uchun
    """
    prefixes = ROLE_PATH_PREFIXES.get(role, [])
    return any(path.startswith(prefix) for prefix in prefixes)


def remove_empty_components(schema):
    """
    Hozircha components qismini o‘chirmaymiz.

    Sababi:
    - paths filtrlangandan keyin ham serializer/schema komponentlari kerak bo‘lishi mumkin;
    - componentsni noto‘g‘ri tozalash Swaggerda $ref xatolarini keltirib chiqaradi.
    """
    return schema


def filter_schema_by_role(schema, role):
    """
    Umumiy OpenAPI schemani olib, faqat tanlangan rolga kerakli endpointlarni qoldiradi.
    """
    filtered = deepcopy(schema)

    paths = filtered.get("paths", {})
    filtered["paths"] = {
        path: item
        for path, item in paths.items()
        if path_allowed(path, role)
    }

    role_label = ROLE_LABELS.get(role, role)

    filtered.setdefault("info", {})
    filtered["info"]["title"] = f"LMS API — {role_label}"
    filtered["info"]["description"] = str(_(
        "Ushbu Swagger hujjati tanlangan rol uchun tegishli endpointlarni ko‘rsatadi. "
        "Backend ruxsatlari permission class orqali server tomonida tekshiriladi."
    ))

    return remove_empty_components(filtered)


class RoleSchemaAPIView(APIView):
    """
    Har bir rol uchun alohida OpenAPI schema qaytaradi.

    Muhim:
    - AllowAny qo‘yildi, chunki Swagger UI schema faylni login qilmasdan yuklay olishi kerak.
    - authentication_classes = [] qo‘yildi, aks holda ayrim holatlarda JWT/session tekshiruv Unauthorized beradi.
    - @extend_schema(exclude=True) qo‘yildi, chunki bu endpoint asosiy openapi.yaml ichiga kirmasligi kerak.
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = None

    @extend_schema(exclude=True)
    def get(self, request, role=None, *args, **kwargs):
        role = role or kwargs.get("role") or request.resolver_match.kwargs.get("role")

        if role not in ROLE_PATH_PREFIXES:
            return JsonResponse(
                {
                    "success": False,
                    "message": str(_("Noto‘g‘ri rol.")),
                    "data": None,
                    "errors": {
                        "role": str(_("Bunday rol uchun Swagger schema mavjud emas."))
                    },
                },
                status=404,
            )

        generator = SchemaGenerator()
        schema = generator.get_schema(request=request, public=True)

        return JsonResponse(
            filter_schema_by_role(schema, role),
            safe=False,
            json_dumps_params={
                "ensure_ascii": False,
                "indent": 2,
            },
        )


class RoleSwaggerView(SpectacularSwaggerView):
    """
    Rolga mos Swagger UI.
    Schema URL role_swagger_urls.py ichida beriladi.
    """
    pass


class RoleRedocView(SpectacularRedocView):
    """
    Rolga mos Redoc UI.
    Schema URL role_swagger_urls.py ichida beriladi.
    """
    pass