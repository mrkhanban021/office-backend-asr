from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver, Signal
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import LogingLog

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
