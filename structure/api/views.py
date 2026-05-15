from core.api.mixins import StandardModelViewSet
from core.api.permissions import ReadOnlyForManagementWriteForAdmin

from structure.models import Organization, Faculty, Department, Specialty, AcademicYear, Semester, Group, Auditorium
from .serializers import (
    OrganizationSerializer,
    FacultySerializer,
    DepartmentSerializer,
    SpecialtySerializer,
    AcademicYearSerializer,
    SemesterSerializer,
    GroupSerializer,
    AuditoriumSerializer,
)


class OrganizationViewSet(StandardModelViewSet):
    queryset = Organization.objects.filter(is_deleted=False).order_by("name")
    serializer_class = OrganizationSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]
    organization_field = "id"


class FacultyViewSet(StandardModelViewSet):
    queryset = Faculty.objects.filter(is_deleted=False).select_related("organization", "dean")
    serializer_class = FacultySerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class DepartmentViewSet(StandardModelViewSet):
    queryset = Department.objects.filter(is_deleted=False).select_related("organization", "faculty", "head")
    serializer_class = DepartmentSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class SpecialtyViewSet(StandardModelViewSet):
    queryset = Specialty.objects.filter(is_deleted=False).select_related("organization", "faculty", "department")
    serializer_class = SpecialtySerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class AcademicYearViewSet(StandardModelViewSet):
    queryset = AcademicYear.objects.filter(is_deleted=False).select_related("organization")
    serializer_class = AcademicYearSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class SemesterViewSet(StandardModelViewSet):
    queryset = Semester.objects.filter(is_deleted=False).select_related("organization", "academic_year")
    serializer_class = SemesterSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class GroupViewSet(StandardModelViewSet):
    queryset = Group.objects.filter(is_deleted=False).select_related("organization", "faculty", "department", "specialty", "academic_year", "curator")
    serializer_class = GroupSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]


class AuditoriumViewSet(StandardModelViewSet):
    queryset = Auditorium.objects.filter(is_deleted=False).select_related("organization")
    serializer_class = AuditoriumSerializer
    permission_classes = [ReadOnlyForManagementWriteForAdmin]
