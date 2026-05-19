from .rbac import (
    get_permission_codes,
    get_primary_assignment,
    get_primary_role_code,
    get_user_assignments,
    get_user_role_codes,
    has_permission,
    has_role,
)


def rbac_context(request):
    user = getattr(request, "user", None)

    if not user or not user.is_authenticated:
        return {
            "rbac_role_codes": set(),
            "rbac_permissions": set(),
            "rbac_primary_role": None,
            "rbac_assignments": [],
        }

    return {
        "rbac_role_codes": get_user_role_codes(user),
        "rbac_permissions": get_permission_codes(user),
        "rbac_primary_role": get_primary_role_code(user),
        "rbac_primary_assignment": get_primary_assignment(user),
        "rbac_assignments": get_user_assignments(user),
        "has_role": lambda *roles: has_role(user, roles),
        "can": lambda code: has_permission(user, code),
    }
