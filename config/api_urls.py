from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.api.urls")),
    path("structure/", include("structure.api.urls")),
    path("academics/", include("academics.api.urls")),
    path("journal/", include("journal.api.urls")),
    path("assessment/", include("assessment.api.urls")),
    path("tasks/", include("tasks.api.urls")),
    path("communication/", include("communication.api.urls")),
    path("documents/", include("documents.api.urls")),
    path("quality/", include("quality.api.urls")),
    path("analytics/", include("analytics.api.urls")),
    path("integrations/", include("integrations.api.urls")),
    path("audit/", include("audit.api.urls")),
]
