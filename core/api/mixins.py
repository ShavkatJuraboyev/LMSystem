from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response

from .permissions import (
    has_any_role,
    user_role_codes,
    get_assignment_scopes,
)
from .roles import (
    MANAGEMENT_ROLES,
    ROLE_ADMIN,
    ROLE_DEAN,
    ROLE_DEPARTMENT_HEAD,
    ROLE_PRORECTOR,
    ROLE_QUALITY_CONTROL,
    ROLE_RECTOR,
    ROLE_STUDENT,
    ROLE_SUPERADMIN,
    ROLE_TEACHER,
)


class CurrentUserCreateUpdateMixin:
    def perform_create(self, serializer):
        kwargs = {}

        if "created_by" in getattr(serializer.Meta.model, "_meta").fields_map:
            kwargs["created_by"] = self.request.user

        try:
            model_fields = [f.name for f in serializer.Meta.model._meta.fields]
            if "created_by" in model_fields:
                kwargs["created_by"] = self.request.user
            if "updated_by" in model_fields:
                kwargs["updated_by"] = self.request.user
        except Exception:
            pass

        serializer.save(**kwargs)

    def perform_update(self, serializer):
        kwargs = {}

        try:
            model_fields = [f.name for f in serializer.Meta.model._meta.fields]
            if "updated_by" in model_fields:
                kwargs["updated_by"] = self.request.user
        except Exception:
            pass

        serializer.save(**kwargs)


class SoftDeleteDestroyMixin:
    """
    DELETE qilganda bazadan o'chirmaydi, is_deleted=True qiladi.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if hasattr(instance, "soft_delete"):
            instance.soft_delete(user=request.user)
            return Response({"detail": "Ma'lumot arxivga o'tkazildi."}, status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)


class OrganizationAutoSetMixin:
    """
    Admin foydalanuvchi obyekt yaratganda organization yubormasa, avtomatik o'z organization'i yoziladi.
    """

    def perform_create(self, serializer):
        model_fields = [f.name for f in serializer.Meta.model._meta.fields]
        save_kwargs = {}

        if "organization" in model_fields and not serializer.validated_data.get("organization"):
            user_org = getattr(self.request.user, "organization", None)
            if user_org:
                save_kwargs["organization"] = user_org

        if "created_by" in model_fields:
            save_kwargs["created_by"] = self.request.user
        if "updated_by" in model_fields:
            save_kwargs["updated_by"] = self.request.user

        serializer.save(**save_kwargs)


class RoleScopedQuerySetMixin:
    """
    Queryset'ni role va scope bo'yicha avtomatik cheklaydi.

    ViewSet ichida kerak bo'lsa quyidagilarni o'zgartiring:
        organization_field = "organization"
        faculty_field = "faculty"
        department_field = "department"
        group_field = "group"
        subject_group_field = "subject_group"
        student_field = "student"
    """

    organization_field = "organization"
    faculty_field = "faculty"
    department_field = "department"
    group_field = "group"
    subject_field = "subject"
    subject_group_field = "subject_group"
    student_field = "student"

    def filter_by_field(self, qs, field_name, value):
        if not field_name or value is None:
            return qs
        try:
            return qs.filter(**{f"{field_name}_id": value})
        except Exception:
            try:
                return qs.filter(**{field_name: value})
            except Exception:
                return qs

    def filter_by_field_in(self, qs, field_name, values):
        if not field_name or not values:
            return qs
        try:
            return qs.filter(**{f"{field_name}_id__in": values})
        except Exception:
            try:
                return qs.filter(**{f"{field_name}__in": values})
            except Exception:
                return qs

    def apply_common_user_filters(self, qs):
        request = self.request

        # Query paramlar.
        allowed_params = {
            "organization": self.organization_field,
            "faculty": self.faculty_field,
            "department": self.department_field,
            "group": self.group_field,
            "subject": self.subject_field,
            "student": self.student_field,
        }

        for param, field in allowed_params.items():
            value = request.query_params.get(param)
            if value:
                qs = self.filter_by_field(qs, field, value)

        # soft delete bo'lsa default ko'rsatilmasin.
        try:
            if "is_deleted" in [f.name for f in qs.model._meta.fields]:
                include_deleted = request.query_params.get("include_deleted") == "1"
                if not include_deleted:
                    qs = qs.filter(is_deleted=False)
        except Exception:
            pass

        return qs

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return qs.none()

        qs = self.apply_common_user_filters(qs)

        if has_any_role(user, [ROLE_SUPERADMIN]):
            return qs

        user_org_id = getattr(user, "organization_id", None)
        if user_org_id and self.organization_field:
            qs = self.filter_by_field(qs, self.organization_field, user_org_id)

        roles = user_role_codes(user)
        scopes = get_assignment_scopes(user)

        if has_any_role(user, [ROLE_ADMIN, ROLE_RECTOR, ROLE_PRORECTOR, ROLE_QUALITY_CONTROL]):
            return qs.distinct()

        if ROLE_DEAN in roles and scopes["faculties"]:
            return self.filter_by_field_in(qs, self.faculty_field, scopes["faculties"]).distinct()

        if ROLE_DEPARTMENT_HEAD in roles and scopes["departments"]:
            return self.filter_by_field_in(qs, self.department_field, scopes["departments"]).distinct()

        if ROLE_TEACHER in roles:
            teacher_q = Q()

            # SubjectGroup modelining o'zi.
            try:
                teacher_q |= Q(main_teacher=user) | Q(assistant_teachers=user)
            except Exception:
                pass

            # Ko'p modelda subject_group orqali bog'langan.
            try:
                teacher_q |= Q(subject_group__main_teacher=user) | Q(subject_group__assistant_teachers=user)
            except Exception:
                pass

            # Topic/LearningContent kabi ichma-ich.
            try:
                teacher_q |= Q(topic__subject_group__main_teacher=user) | Q(topic__subject_group__assistant_teachers=user)
            except Exception:
                pass

            # AssignmentSubmission kabi.
            try:
                teacher_q |= Q(assignment__subject_group__main_teacher=user) | Q(assignment__subject_group__assistant_teachers=user)
            except Exception:
                pass

            # TestAttempt/StudentAnswer kabi.
            try:
                teacher_q |= Q(test__subject_group__main_teacher=user) | Q(test__subject_group__assistant_teachers=user)
            except Exception:
                pass

            if teacher_q:
                try:
                    return qs.filter(teacher_q).distinct()
                except Exception:
                    pass

        if ROLE_STUDENT in roles:
            student_profile = getattr(user, "student_profile", None)
            if not student_profile:
                return qs.none()

            student_q = Q()

            # StudentProfile modelining o'zi.
            try:
                student_q |= Q(id=student_profile.id)
            except Exception:
                pass

            # Grade/Attendance/Submission/Attempt.
            try:
                student_q |= Q(student=student_profile)
            except Exception:
                pass

            try:
                student_q |= Q(attempt__student=student_profile)
            except Exception:
                pass

            # Talaba uchun fan-guruhlar.
            try:
                student_q |= Q(group=student_profile.group)
            except Exception:
                pass

            try:
                student_q |= Q(subject_group__group=student_profile.group)
            except Exception:
                pass

            if student_q:
                try:
                    return qs.filter(student_q).distinct()
                except Exception:
                    pass

        return qs.none()


class StandardModelViewSet(
    SoftDeleteDestroyMixin,
    OrganizationAutoSetMixin,
    CurrentUserCreateUpdateMixin,
    RoleScopedQuerySetMixin,
    viewsets.ModelViewSet,
):
    pass


class StandardReadOnlyViewSet(RoleScopedQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    pass
