from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ModuleViewSet, PermissionViewSet, RoleViewSet, RolePermissionViewSet, UserRoleAssignmentViewSet, EmployeeProfileViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"modules", ModuleViewSet, basename="modules")
router.register(r"permissions", PermissionViewSet, basename="permissions")
router.register(r"roles", RoleViewSet, basename="roles")
router.register(r"role-permissions", RolePermissionViewSet, basename="role-permissions")
router.register(r"user-roles", UserRoleAssignmentViewSet, basename="user-roles")
router.register(r"employees", EmployeeProfileViewSet, basename="employees")
router.register(r"students", StudentProfileViewSet, basename="students")

urlpatterns = router.urls
