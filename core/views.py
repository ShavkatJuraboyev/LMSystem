from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.rbac import DASHBOARD_TEMPLATE_MAP, get_primary_role_code


@login_required(login_url="/accounts/login/")
def dashboard(request):
    role_code = get_primary_role_code(request.user)

    if not role_code:
        return render(request, "errors/no_role.html")

    template = DASHBOARD_TEMPLATE_MAP.get(role_code, "dashboards/custom.html")
    return render(request, template, {
        "active_role": role_code,
    })
