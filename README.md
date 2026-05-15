# LMSystem
Online learning system

# Universitet/Institut LMS — alohida app'larga bo'lingan Django database arxitekturasi

Ushbu arxitektura katta LMS tizimi uchun professional tarzda app'larga ajratilgan.

## App'lar

- `core` — umumiy choices, abstract base modellari, soft delete
- `accounts` — User, Role, Permission, UserRoleAssignment, StudentProfile, EmployeeProfile
- `structure` — Organization, Faculty, Department, Specialty, AcademicYear, Semester, Group, Auditorium
- `academics` — Curriculum, Subject, SubjectGroup, Topic, LearningContent
- `journal` — Schedule, LessonSession, Attendance
- `assessment` — AssessmentType, Grade, GradeHistory, Appeal
- `tasks` — Assignment, Submission, QuestionBank, Test
- `communication` — Announcement, DirectMessage, SupportRequest
- `documents` — OfficialDocument, DocumentApproval
- `quality` — QualityInspection, Deficiency, Survey
- `analytics` — KPISnapshot, RiskAlert
- `integrations` — IntegrationConfig, IntegrationLog, BackupLog, SystemHealthLog
- `audit` — AuditLog, LoginHistory, ExportLog, SecurityEvent

## settings.py

```python
INSTALLED_APPS = [
    # ...
    "core",
    "structure",
    "accounts",
    "academics",
    "journal",
    "assessment",
    "tasks",
    "communication",
    "documents",
    "quality",
    "analytics",
    "integrations",
    "audit",
]

AUTH_USER_MODEL = "accounts.User"
```

## Migratsiya tartibi

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```



# LMS API fayllari — Django REST Framework

Bir app uchun API fayllar bor:

- `api/serializers.py`
- `api/views.py`
- `api/urls.py`

Qo'shimcha:

- `core/api/permissions.py`
- `core/api/mixins.py`
- `config/api_urls.py`

## O'rnatish

```bash
pip install djangorestframework django-filter
```

## settings.py

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "django_filters",

    "core",
    "structure",
    "accounts",
    "academics",
    "journal",
    "assessment",
    "tasks",
    "communication",
    "documents",
    "quality",
    "analytics",
    "integrations",
    "audit",
]

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

## config/urls.py

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("config.api_urls")),
]
```

## Rollar bo'yicha ruxsat mantiqi

- Superadmin: hammasini ko'radi/boshqaradi.
- Admin: o'z muassasasi doirasida boshqaradi.
- Rektor/Prorektor: muassasa doirasida ko'radi, ayrim workflowlarda tasdiqlaydi.
- Dekan: o'z fakulteti doirasida ko'radi/nazorat qiladi.
- Kafedra mudiri: o'z kafedrasi doirasida ko'radi/nazorat qiladi.
- O'qituvchi: o'z fan/guruh/topshiriq/test/jurnalini boshqaradi.
- Talaba: o'z bahosi, davomadi, topshirig'i, testi va murojaatini ko'radi/bajaradi.
- Ta'lim sifati nazorati: sifat monitoringi, survey, deficiency, KPI bo'yicha ishlaydi.

## JWT tavsiya

Production uchun BasicAuthentication o'rniga JWT ishlating:

```bash
pip install djangorestframework-simplejwt
```

settings.py:

```python
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
]
```

urls.py:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```