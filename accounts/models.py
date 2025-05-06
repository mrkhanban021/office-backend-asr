from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
import os
from django.utils import timezone
import random
import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("phone number is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if not password:
            raise ValueError("superuser must have password.")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        EMPLOYEE = 'employee', 'Employee'
        GUARD = 'guard', 'Guard'
        USER = 'user', 'User'

    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, null=True, blank=True, choices=RoleChoices.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        profile = self.profile
        return f'{self.phone_number} ({profile.name} {profile.last_name})'

    class Meta:
        verbose_name = "USER"
        verbose_name_plural = "USER"


def validate_national_code(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("کد ملی باید دقیقا 10 رقم باشد.")
    check = int(value[9])
    s = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
    if not ((s < 2 and check == s) or (s >= 2 and check + s == 11)):
        raise ValidationError("کد ملی نامعتبر است.")


def avatar_upload_to(instance, filename):
    return os.path.join('avatars', f'user_{instance.id}', filename)


class ProfileUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    id_code = models.CharField(max_length=10, null=True, blank=True, validators=[validate_national_code])
    address = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ProfileUser"
        verbose_name_plural = "ProfileUser"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=['id_code'],
                name='unique_id_code_not_null',
                condition=~models.Q(id_code=None)
            )
        ]

    def __str__(self):
        return f'{self.name} {self.last_name}'


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = str(random.randint(100000, 999999))
            self.expires_at = timezone.now() + datetime.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.user.phone_number} - Code: {self.code}"

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = 'OTP'


class OTPRequest(models.Model):
    otp = models.ForeignKey(OTP, on_delete=models.CASCADE, null=True)
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp.user.phone_number

    class Meta:
        verbose_name = "OTPRequest"
        verbose_name_plural = "OTPRequest"
