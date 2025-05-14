from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ProfileUser, OTP, OTPRequest


@receiver(post_save, sender=CustomUser)
def create_user_profile_for_user(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)


@receiver(post_save, sender=OTP)
def create_otp_request(sender, instance, created, **kwargs):
    if created:
        OTPRequest.objects.create(otp=instance)