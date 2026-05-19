from django import forms
from django.contrib.auth import get_user_model

from .models import Permission, Role, UserRoleAssignment


class BootstrapFormMixin:
    def _add_bootstrap_classes(self):
        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": "form-check-input"})
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs.update({"class": "form-check-input"})
            elif isinstance(widget, forms.SelectMultiple):
                widget.attrs.update({"class": "form-select"})
            elif isinstance(widget, forms.Select):
                widget.attrs.update({"class": "form-select"})
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({"class": "form-control"})
            else:
                widget.attrs.update({"class": "form-control"})


class RoleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Role
        fields = [
            "organization",
            "name",
            "code",
            "role_type",
            "description",
            "is_system",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_bootstrap_classes()


class RolePermissionForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("module").all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Ruxsatlar",
    )

    def __init__(self, *args, role=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role
        self.fields["permissions"].queryset = Permission.objects.select_related("module").order_by("module__name", "action")

        if role and not self.is_bound:
            self.initial["permissions"] = role.role_permissions.values_list("permission_id", flat=True)


class UserRoleAssignmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UserRoleAssignment
        fields = [
            "user",
            "role",
            "organization",
            "faculty",
            "department",
            "group",
            "subject",
            "starts_at",
            "ends_at",
            "is_active",
        ]
        widgets = {
            "starts_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "ends_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_bootstrap_classes()

    def clean(self):
        cleaned = super().clean()
        user = cleaned.get("user")
        role = cleaned.get("role")
        organization = cleaned.get("organization")
        faculty = cleaned.get("faculty")
        department = cleaned.get("department")
        group = cleaned.get("group")
        subject = cleaned.get("subject")

        if user and role:
            qs = UserRoleAssignment.objects.filter(
                user=user,
                role=role,
                organization=organization,
                faculty=faculty,
                department=department,
                group=group,
                subject=subject,
                is_active=True,
            )

            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Ushbu foydalanuvchiga bu rol aynan shu scope bilan oldin biriktirilgan.")

        return cleaned


class MultiRoleAssignmentForm(BootstrapFormMixin, forms.Form):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(is_active=True).order_by("username"),
        label="Foydalanuvchi",
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.filter(is_active=True).order_by("role_type", "name"),
        label="Rollar",
        help_text="Bitta foydalanuvchiga bir nechta rol tanlash mumkin.",
        widget=forms.SelectMultiple,
    )
    organization = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Muassasa",
    )
    faculty = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Fakultet",
    )
    department = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Kafedra",
    )
    group = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Guruh",
    )
    subject = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Fan",
    )
    starts_at = forms.DateTimeField(
        required=False,
        label="Boshlanish",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    ends_at = forms.DateTimeField(
        required=False,
        label="Tugash",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label="Faol",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from structure.models import Department, Faculty, Group, Organization
        from academics.models import Subject

        self.fields["organization"].queryset = Organization.objects.all()
        self.fields["faculty"].queryset = Faculty.objects.all()
        self.fields["department"].queryset = Department.objects.all()
        self.fields["group"].queryset = Group.objects.all()
        self.fields["subject"].queryset = Subject.objects.all()

        self._add_bootstrap_classes()
