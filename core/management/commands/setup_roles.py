from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import SAPPermission

class Command(BaseCommand):
    help = 'Erstellt die Standard-Gruppen und weist Rechte zu'

    def handle(self, *args, **options):
        # Hole den ContentType für unser SAPPermission Modell
        ct = ContentType.objects.get_for_model(SAPPermission)

        # Definition der Rollen und ihrer Rechte
        roles = {
            "Viewer": [
                "sap_view_dashboard",
                "sap_view_equipments", 
                "sap_view_orders"
            ],
            "Maschinenbediener": [
                "sap_view_dashboard",
                "sap_view_equipments", 
                "sap_view_orders",
                "sap_create_order"
            ],
            "Instandhalter": [
                "sap_view_dashboard",
                "sap_view_equipments", 
                "sap_view_orders",
                "sap_edit_own_orders",
                "sap_confirm_order"
            ],
            "Koordinator": [
                "sap_view_dashboard", "sap_view_equipments", "sap_view_orders",
                "sap_create_order", "sap_edit_own_orders", "sap_confirm_order",
                "sap_edit_all_orders", "sap_release_order", "sap_technical_complete"
            ]
        }

        for role_name, permissions in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(f"Gruppe '{role_name}' erstellt.")
            
            for perm_code in permissions:
                try:
                    perm = Permission.objects.get(codename=perm_code, content_type=ct)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Recht '{perm_code}' nicht gefunden! Hast du migriert?"))

            self.stdout.write(self.style.SUCCESS(f"Rechte für '{role_name}' aktualisiert."))