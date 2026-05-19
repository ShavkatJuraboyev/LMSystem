from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from structure.models import Organization

from .forms import MultiRoleAssignmentForm, RoleForm, RolePermissionForm, UserRoleAssignmentForm
from .models import Permission, Role, RolePermission, UserRoleAssignment
from .rbac import ROLE_SUPERADMIN, permission_required, role_required

 
def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            "Login yoki parol noto‘g‘ri"
        )

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Siz muvaffaqiyatli tizimdan chiqdingiz.")
    return redirect("login")


@login_required
@permission_required("roles.view")
def role_list(request):
    roles = Role.objects.select_related("organization").prefetch_related("role_permissions")

    q = request.GET.get("q")
    status = request.GET.get("status")

    if q:
        roles = roles.filter(
            Q(name__icontains=q) |
            Q(code__icontains=q) |
            Q(description__icontains=q)
        )

    if status == "active":
        roles = roles.filter(is_active=True)
    elif status == "inactive":
        roles = roles.filter(is_active=False)

    context = {
        "roles": roles.order_by("role_type", "name"),
        "active_roles_count": Role.objects.filter(is_active=True).count(),
        "inactive_roles_count": Role.objects.filter(is_active=False).count(),
        "system_roles_count": Role.objects.filter(is_system=True).count(),
        "permissions_count": Permission.objects.count(),
    }
    return render(request, "accounts/roles/role_list.html", context)


@login_required
@permission_required("roles.create")
def role_create(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol muvaffaqiyatli yaratildi.")
            return redirect("role_list")
    else:
        form = RoleForm()

    return render(request, "accounts/roles/role_form.html", {
        "form": form,
        "title": "Yangi rol yaratish",
    })


@login_required
@permission_required("roles.update")
def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)

    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol muvaffaqiyatli yangilandi.")
            return redirect("role_list")
    else:
        form = RoleForm(instance=role)

    return render(request, "accounts/roles/role_form.html", {
        "form": form,
        "title": "Rolni tahrirlash",
    })


@login_required
@permission_required("roles.delete")
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)

    if role.is_system:
        messages.error(request, "Tizim rolini o‘chirish mumkin emas.")
        return redirect("role_list")

    if request.method == "POST":
        role.delete()
        messages.success(request, "Rol o‘chirildi.")

    return redirect("role_list")


@login_required
def role_permission_update(request, pk):
    role = get_object_or_404(Role, pk=pk)

    permissions = Permission.objects.select_related("module").all()

    grouped_permissions = {}

    for permission in permissions:
        module = permission.module

        if module not in grouped_permissions:
            grouped_permissions[module] = []

        grouped_permissions[module].append(permission)

    selected_permission_ids = list(
        RolePermission.objects.filter(role=role)
        .values_list("permission_id", flat=True)
    )

    if request.method == "POST":

        permission_ids = request.POST.getlist("permissions")

        RolePermission.objects.filter(role=role).delete()

        role_permissions = []

        for permission_id in permission_ids:

            role_permissions.append(
                RolePermission(
                    role=role,
                    permission_id=permission_id
                )
            )

        RolePermission.objects.bulk_create(role_permissions)

        messages.success(request, "Rol ruxsatlari saqlandi.")

        return redirect("role_list")

    context = {
        "role": role,
        "grouped_permissions": grouped_permissions,
        "selected_permission_ids": selected_permission_ids,
    }

    return render(
        request,
        "accounts/roles/role_permission_form.html",
        context
    )


@login_required
@permission_required("roles.view")
def user_role_list(request):
    user_roles = UserRoleAssignment.objects.select_related(
        "user", "role", "organization", "faculty", "department", "group", "subject"
    )

    q = request.GET.get("q")
    if q:
        user_roles = user_roles.filter(
            Q(user__username__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(role__name__icontains=q)
        )

    return render(request, "accounts/roles/user_role_list.html", {
        "user_roles": user_roles.order_by("-created_at"),
    })


@login_required
@permission_required("roles.manage")
def user_role_create(request):
    if request.method == "POST":
        form = UserRoleAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Foydalanuvchiga rol biriktirildi.")
            return redirect("user_role_list")
    else:
        form = UserRoleAssignmentForm()

    return render(request, "accounts/roles/user_role_form.html", {
        "form": form,
        "title": "Foydalanuvchiga rol biriktirish",
    })


@login_required 
@permission_required("roles.manage")
def user_multi_role_create(request):
    """
    Bitta foydalanuvchiga 2 yoki 3 ta emas, istalgancha rolni bir marta orqali biriktiradi.
    """
    if request.method == "POST":
        form = MultiRoleAssignmentForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            roles = form.cleaned_data["roles"]

            created_count = 0

            common_data = {
                "user": user,
                "organization": form.cleaned_data.get("organization"),
                "faculty": form.cleaned_data.get("faculty"),
                "department": form.cleaned_data.get("department"),
                "group": form.cleaned_data.get("group"),
                "subject": form.cleaned_data.get("subject"),
                "starts_at": form.cleaned_data.get("starts_at"),
                "ends_at": form.cleaned_data.get("ends_at"),
                "is_active": form.cleaned_data.get("is_active"),
            }

            for role in roles:
                _, created = UserRoleAssignment.objects.get_or_create(
                    user=user,
                    role=role,
                    organization=common_data["organization"],
                    faculty=common_data["faculty"],
                    department=common_data["department"],
                    group=common_data["group"],
                    subject=common_data["subject"],
                    defaults={
                        "starts_at": common_data["starts_at"],
                        "ends_at": common_data["ends_at"],
                        "is_active": common_data["is_active"],
                    }
                )
                if created:
                    created_count += 1

            messages.success(request, f"{user} foydalanuvchisiga {created_count} ta yangi rol biriktirildi.")
            return redirect("user_role_list")
    else:
        form = MultiRoleAssignmentForm()

    return render(request, "accounts/roles/user_multi_role_form.html", {
        "form": form,
        "title": "Foydalanuvchiga bir nechta rol biriktirish",
    })


@login_required
@permission_required("roles.manage")
def user_role_edit(request, pk):
    user_role = get_object_or_404(UserRoleAssignment, pk=pk)

    if request.method == "POST":
        form = UserRoleAssignmentForm(request.POST, instance=user_role)
        if form.is_valid():
            form.save()
            messages.success(request, "Foydalanuvchi roli yangilandi.")
            return redirect("user_role_list")
    else:
        form = UserRoleAssignmentForm(instance=user_role)

    return render(request, "accounts/roles/user_role_form.html", {
        "form": form,
        "title": "Foydalanuvchi rolini tahrirlash",
    })


@login_required
@permission_required("roles.manage")
def user_role_delete(request, pk):
    user_role = get_object_or_404(UserRoleAssignment, pk=pk)

    if request.method == "POST":
        user_role.delete()
        messages.success(request, "Biriktirilgan rol o‘chirildi.")

    return redirect("user_role_list")

