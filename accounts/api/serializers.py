from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
            "email",
            "phone",
            "passport_pinfl",
            "birth_date",
            "gender",
            "avatar",
            "organization",
            "status",
            "two_factor_enabled",
            "last_activity_at",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined", "last_activity_at", "two_factor_enabled")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "passport_pinfl",
            "birth_date",
            "gender",
            "organization",
            "status",
            "is_active",
            "is_staff",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class UserRoleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleAssignment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")


class StudentProfileSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source="user.full_name", read_only=True)
    group_name = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by")
