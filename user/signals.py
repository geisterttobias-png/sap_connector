from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile_and_assign_default_group(sender, instance, created, **kwargs):
    """
    Sobald ein neuer User erstellt wird (z.B. via SSO),
    erstellen wir das Profil und weisen die Gruppe 'Viewer' zu.
    """
    if created:
        # 1. Profil anlegen
        UserProfile.objects.create(user=instance)

        # 2. In 'Viewer' Gruppe stecken
        # get_or_create verhindert Fehler, falls die Gruppe noch nicht existiert
        viewer_group, _ = Group.objects.get_or_create(name='Viewer')
        instance.groups.add(viewer_group)
