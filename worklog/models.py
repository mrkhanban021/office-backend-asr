import os.path

from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

USER = get_user_model()


class LogingLog(models.Model):
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number} - {self.login_time}'

    class Meta:
        verbose_name = "LogingLog"
        verbose_name_plural = "LogingLog"


class Department(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True,)
    created_time = models.DateTimeField(auto_now_add=True,)
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Department"
        ordering = ("-created_time",)

    def __str__(self):
        return self.title


def employee_upload_path(instance, filename, filetype):
    folder_name = slugify(f"{instance.first_name} {instance.last_name}")
    ext = os.path.splitext(filename)[1]  # مثل .jpg یا .png
    return os.path.join("employee", folder_name, f"{filetype}{ext}")


def avatar_upload_path(instance, filename):
    return employee_upload_path(instance, filename, "avatar")


def signature_upload_path(instance, filename):
    return employee_upload_path(instance, filename, "signature")


def fingerprint_upload_path(instance, filename):
    return employee_upload_path(instance, filename, "fingerprint")


def validate_national_code(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("کد ملی باید دقیقا 10 رقم باشد.")
    check = int(value[9])
    s = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
    if not ((s < 2 and check == s) or (s >= 2 and check + s == 11)):
        raise ValidationError("کد ملی نامعتبر است.")


class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="department")
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    hire_date = jmodels.jDateField(null=True, blank=True)
    position = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_of_birth = jmodels.jDateField(null=True, blank=True)
    id_code = models.CharField(max_length=10, unique=True, validators=[validate_national_code])
    signature_image = models.ImageField(upload_to=signature_upload_path, null=True, blank=True)
    fingerprint_image = models.ImageField(upload_to=fingerprint_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employee"
        ordering = ("-created_at",)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ToolCategory(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True, verbose_name="toolCategory")

    class Meta:
        verbose_name = "ToolCategory"
        verbose_name_plural = "ToolCategory"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Tools(models.Model):
    ToolCategory = models.ForeignKey(ToolCategory, on_delete=models.SET_NULL, null=True, verbose_name="ToolCategory_tools")
    title = models.CharField(max_length=100, null=True, blank=True)
    seria_number = models.CharField(max_length=50, blank=True, unique=True)
    counting = models.IntegerField(default=0, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="department_tools")

    class Meta:
        verbose_name = "Tools"
        verbose_name_plural = "Tools"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class ToolTransferLog(models.Model):
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE, related_name="transfer_logs")
    employee = models.ForeignKey(Employee, models.CASCADE, related_name="tool_transfers")

    taken_at = jmodels.jDateField(null=True, blank=True)
    returned_at = jmodels.jDateField(null=True, blank=True)

    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def is_returned(self):
        return self.returned_at is not None

    def __str__(self):
        return f'{self.tool.title} {self.employee.first_name} {self.employee.last_name}'

    class Meta:
        verbose_name = "ToolTransferLog"
        verbose_name_plural = "ToolTransferLog"
        ordering = ("-created_at",)


class EntryExitLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="entry_exit_logs")

    exit_time = jmodels.jDateTimeField(auto_now_add=True)
    entry_time = models.TimeField(null=True, blank=True)

    reason = models.TextField(null=True, blank=True)
    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_returned(self):
        if self.entry_time:
            return self.entry_time - self.exit_time
        return None

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.exit_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "EntryExitLog"
        verbose_name_plural = "EntryExitLog"
        ordering = ("-created_at",)


class PeopleCategory(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PeopleCategory"
        verbose_name_plural = "PeopleCategory"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class ExternalPerson(models.Model):
    category = models.ForeignKey(PeopleCategory, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    national_code = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    compony = models.CharField(max_length=100, null=True, blank=True)

    centered_at = jmodels.jDateTimeField(auto_now_add=True)
    exit = models.TimeField(null=True, blank=True)
    notex = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "ExternalPerson"
        verbose_name_plural = "ExternalPerson"
        ordering = ("-centered_at",)

    def __str__(self):
        return self.full_name







