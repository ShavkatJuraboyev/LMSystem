from django.core.management.base import BaseCommand
from accounts.models import Module, Permission, Role


class Command(BaseCommand):
    help = "RBAC tizimi uchun boshlang‘ich ma’lumotlarni yaratadi"

    def handle(self, *args, **kwargs):
        modules = [
            ("users", "Foydalanuvchilar"),
            ("roles", "Rollar"),
            ("students", "Talabalar"),
            ("teachers", "O‘qituvchilar"),
            ("departments", "Kafedralar"),
            ("faculties", "Fakultetlar"),
            ("groups", "Guruhlar"),
            ("subjects", "Fanlar"),
            ("attendance", "Davomat"),
            ("grades", "Baholar"),
            ("schedule", "Dars jadvali"),
            ("reports", "Hisobotlar"),
            ("quality", "Sifat nazorati"),
            ("settings", "Sozlamalar"),
        ]

        actions = [
            ("view", "Ko‘rish"),
            ("create", "Yaratish"),
            ("update", "Tahrirlash"),
            ("delete", "O‘chirish"),
            ("manage", "Boshqarish"),
            ("export", "Eksport"),
            ("import", "Import"),
            ("approve", "Tasdiqlash"),
        ]

        for module_code, module_name in modules:
            module, _ = Module.objects.get_or_create(
                code=module_code,
                defaults={
                    "name": module_name,
                    "description": f"{module_name} moduli",
                    "is_active": True,
                }
            )

            for action_code, action_name in actions:
                Permission.objects.get_or_create(
                    module=module,
                    action=action_code,
                    defaults={
                        "code": f"{module_code}.{action_code}",
                        "name": f"{module_name} - {action_name}",
                        "description": f"{module_name} uchun {action_name} ruxsati",
                    }
                )

        roles = [
            ("superadmin", "Superadmin", "superadmin"),
            ("admin", "Admin", "admin"),
            ("rector", "Rektor", "rector"),
            ("prorector", "Prorektor", "prorector"),
            ("dean", "Dekan", "dean"),
            ("department_head", "Kafedra mudiri", "department_head"),
            ("teacher", "O‘qituvchi", "teacher"),
            ("student", "Talaba", "student"),
            ("quality_control", "Sifat nazorati", "quality_control"),
        ]

        for code, name, role_type in roles:
            Role.objects.get_or_create(
                organization=None,
                code=code,
                defaults={
                    "name": name,
                    "role_type": role_type,
                    "description": f"{name} tizim roli",
                    "is_system": True,
                    "is_active": True,
                }
            )

        self.stdout.write(self.style.SUCCESS("RBAC ma’lumotlari yaratildi."))