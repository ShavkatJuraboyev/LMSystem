from django.urls import path

from core.api.schema import RoleSchemaAPIView, RoleSwaggerView, RoleRedocView


ROLE_URLS = {
    "superadmin": "superadmin",
    "admin": "admin",
    "rector": "rector",
    "prorector": "prorector",
    "dean": "dean",
    "department_head": "department-head",
    "teacher": "teacher",
    "student": "student",
    "quality_control": "quality-control",
}

urlpatterns = []

for role, url_part in ROLE_URLS.items():
    urlpatterns += [
        path(f"schema/{url_part}/", RoleSchemaAPIView.as_view(), {"role": role}, name=f"schema-{url_part}"),
        path(f"swagger/{url_part}/", RoleSwaggerView.as_view(url_name=f"schema-{url_part}"), name=f"swagger-{url_part}"),
        path(f"redoc/{url_part}/", RoleRedocView.as_view(url_name=f"schema-{url_part}"), name=f"redoc-{url_part}"),
    ]