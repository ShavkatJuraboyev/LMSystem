from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet, FacultyViewSet, DepartmentViewSet, SpecialtyViewSet, AcademicYearViewSet, SemesterViewSet, GroupViewSet, AuditoriumViewSet

router = DefaultRouter()
router.register(r"organizations", OrganizationViewSet, basename="organizations")
router.register(r"faculties", FacultyViewSet, basename="faculties")
router.register(r"departments", DepartmentViewSet, basename="departments")
router.register(r"specialties", SpecialtyViewSet, basename="specialties")
router.register(r"academic-years", AcademicYearViewSet, basename="academic-years")
router.register(r"semesters", SemesterViewSet, basename="semesters")
router.register(r"groups", GroupViewSet, basename="groups")
router.register(r"auditoriums", AuditoriumViewSet, basename="auditoriums")

urlpatterns = router.urls
