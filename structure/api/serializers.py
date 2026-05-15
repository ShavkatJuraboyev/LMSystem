from rest_framework import serializers

from structure.models import Organization, Faculty, Department, Specialty, AcademicYear, Semester, Group, Auditorium


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")
