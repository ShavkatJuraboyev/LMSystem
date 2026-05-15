from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import UserRoleAssignment


ROLE_TEMPLATE_MAP = {
    "superadmin": "dashboards/superadmin.html",
    "admin": "dashboards/admin.html",
    "rector": "dashboards/rector.html",
    "prorector": "dashboards/prorector.html",
    "dean": "dashboards/dean.html",
    "department_head": "dashboards/department_head.html",
    "teacher": "dashboards/teacher.html",
    "student": "dashboards/student.html",
    "quality_control": "dashboards/quality.html",
}


@login_required(login_url="/accounts/login/")
def dashboard(request):

    user_role = (
        UserRoleAssignment.objects
        .select_related("role")
        .filter(
            user=request.user,
            is_active=True
        )
        .first()
    )

    if not user_role:
        return render(
            request,
            "errors/no_role.html"
        )

    role_code = user_role.role.role_type

    template = ROLE_TEMPLATE_MAP.get(role_code)

    if not template:
        return render(
            request,
            "errors/no_role.html"
        )

    return render(request, template)