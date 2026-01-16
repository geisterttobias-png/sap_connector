from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Erweitert den Standard-User um SAP-spezifische Felder.
    """
    # Verknüpfung 1:1 zum Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Welches Werk darf der User sehen? (z.B. '1000'). Leer = Alle.
    sap_plant = models.CharField(max_length=4, blank=True, null=True, verbose_name="SAP Werk")

    # Personalnummer (wichtig, wenn der User Aufträge anlegt -> 'Gemeldet von')
    sap_personnel_number = models.CharField(max_length=20, blank=True, verbose_name="Personalnr.")

    def __str__(self):
        return f"Profil: {self.user.username}"

class SAPPermission(models.Model):
    """
    Ein 'Dummy'-Modell, das nur dazu dient, unsere individuellen
    SAP-Rechte in der Django-Datenbank zu registrieren.
    Es wird nie Daten enthalten (managed=False).
    """
    class Meta:
        managed = False  # Keine echte Tabelle in der DB
        default_permissions = () # Standard add/change/delete deaktivieren
        permissions = [
            # Viewer
            ("sap_view_dashboard", "Darf Dashboard sehen"),
            ("sap_view_equipments", "Darf Anlagen sehen"),
            ("sap_view_orders", "Darf Aufträge lesen"),

            # Maschinenbediener
            ("sap_create_order", "Darf Auftrag/Meldung anlegen"),

            # Instandhalter
            ("sap_edit_own_orders", "Darf eigene Aufträge bearbeiten"),
            ("sap_confirm_order", "Darf Zeitrückmeldung buchen"),

            # Koordinator
            ("sap_edit_all_orders", "Darf alle Aufträge bearbeiten"),
            ("sap_release_order", "Darf Aufträge freigeben"),
            ("sap_technical_complete", "Darf technisch abschließen (TECO)"),
        ]
