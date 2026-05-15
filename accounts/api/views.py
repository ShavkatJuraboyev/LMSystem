from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.mixins import StandardModelViewSet
from core.api.permissions import IsAdminOrSuperAdmin, IsAuthenticatedAndActive, ReadOnlyForManagementWriteForAdmin

from accounts.models import (
    User,
    Module,
    Permission,
    Role,
    RolePermission,
    UserRoleAssignment,
    EmployeeProfile,
    StudentProfile,
)
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    ModuleSerializer,
    PermissionSerializer,
    RoleSerializer,
    RolePermissionSerializer,
    UserRoleAssignmentSerializer,
    EmployeeProfileSerializer,
    StudentProfileSerializer,
)


class UserViewSet(StandardModelViewSet):
    queryset = User.objects.all().select_related("organization")
    permission_classes = [IsAdminOrSuperAdmin]
    organization_field = "organization"

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticatedAndActive])
    def me(self, request):
        return Response(UserSerializer(request.user, context={"request": request}).data)


class ModuleViewSet(StandardModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class PermissionViewSet(StandardModelViewSet):
    queryset = Permission.objects.all().select_related("module")
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class RoleViewSet(StandardModelViewSet):
    queryset = Role.objects.filter(is_deleted=False).select_related("organization")
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class RolePermissionViewSet(StandardModelViewSet):
    queryset = RolePermission.objects.all().select_related("role", "permission")
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class UserRoleAssignmentViewSet(StandardModelViewSet):
    queryset = UserRoleAssignment.objects.filter(is_deleted=False).select_related("user", "role", "organization", "faculty", "department", "group", "subject")
    serializer_class = UserRoleAssignmentSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class EmployeeProfileViewSet(StandardModelViewSet):
    queryset = EmployeeProfile.objects.filter(is_deleted=False).select_related("user", "organization", "faculty", "department")
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class StudentProfileViewSet(StandardModelViewSet):
    queryset = StudentProfile.objects.filter(is_deleted=False).select_related("user", "organization", "faculty", "department", "specialty", "group")
    serializer_class = StudentProfileSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]
