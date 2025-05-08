import os.path
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import LogingLog, Employee
from django.utils.text import slugify
from django.conf import settings

USER = get_user_model()
user_logged_in_signal = Signal()


@receiver(user_logged_in_signal)
def log_user_login(sender, request, user, **kwargs):
    profile = getattr(user, 'profile', None)
    full_name = f"{profile.name} {profile.last_name} " if profile else ""
    LogingLog.objects.create(
        user=user,
        phone_number=user.phone_number,
        full_name=full_name,
        role=user.role
    )


@receiver(post_save, sender=Employee)
def create_employee_folder(sender, instance, created, **kwargs):
    if created:
        folder_name = slugify(f"{instance.first_name} {instance.last_name}")
        employee_folder_path = os.path.join(settings.MEDIA_ROOT, "employee", folder_name)
        os.makedirs(employee_folder_path, exist_ok=True)
