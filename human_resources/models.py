from django.db import models
from worklog.models import Employee
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import jdatetime
from django_jalali.db import models as jmodels
import os

USER = get_user_model()


def fingerprint_upload_path(instance, filename):
    if instance.employee:
        folder_name = slugify(f"{instance.employee.first_name} {instance.employee.last_name}")
    elif instance.full_name:
        folder_name = slugify(instance.full_name)
    else:
        folder_name = "unknown"

    return os.path.join('employee', folder_name, 'fingerprint', filename)


class AssistanceRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    fingerprint_image = models.ImageField(upload_to=fingerprint_upload_path, null=True, blank=True)
    loan_installment = models.BooleanField(default=False)
    installment_amount = models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=2) # مبلغ قسط
    total_installments = models.PositiveIntegerField(null=True, blank=True) #تعداد کل اقساط
    paid_installments = models.PositiveIntegerField(default=0) # چند قسط پرداخت شده
    account_number = models.CharField(max_length=30, blank=True, null=True) # شماره حساب (در صورت نیاز)
    card_number = models.CharField(max_length=30, blank=True, null=True) # شماره کارت
    sheba_number = models.CharField(max_length=35, null=True, blank=True) # شماره شبا
    explanation = models.TextField(null=True, blank=True)  # توضیحات درباره دلیل درخواست مساعده

    # وضعیت تایید

    manager_approval = models.BooleanField(default=False)
    admin_approval = models.BooleanField(default=False)
    ceo_approval = models.BooleanField(default=False)

    final_approval = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_all_approvals(self):
        return self.manager_approval and self.admin_approval and self.ceo_approval

    def update_final_approval(self):
        self.final_approval = self.check_all_approvals()
        self.save()

    def save(self, *args, **kwargs):
        if self.employee:
            self.full_name = f'{self.employee.first_name} {self.employee.last_name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "AssistanceRequest"
        verbose_name_plural = "AssistanceRequest"
        ordering = ("-request_date",)


class MonthlyAssistanceSummary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    total_assistance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.employee:
            self.full_name = f'{self.employee.first_name} {self.employee.last_name}'
        super().save(*args, **kwargs)

    @staticmethod
    def update_summary(employee, amount):
        now = timezone.now()
        print(f"{employee} {amount}")
        shamsi_date = jdatetime.date.fromgregorian(year=now.year, month=now.month, day=now.day)
        shamsi_year = shamsi_date.year
        shamsi_month = shamsi_date.month

        summary, created = MonthlyAssistanceSummary.objects.get_or_create(employee=employee, year=shamsi_year,
                                                                          month=shamsi_month)
        summary.total_assistance += amount
        summary.save()

    class Meta:
        verbose_name = "MonthlyAssistanceSummary"
        verbose_name_plural = "MonthlyAssistanceSummary"
        ordering = ("-create_at",)


class BankAccount(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(null=True, blank=True, max_length=100)
    title = models.CharField(max_length=20, null=True,blank=True)
    account_number = models.CharField(max_length=30, null=True, blank=True)
    card_number = models.CharField(max_length=30, null=True, blank=True)
    sheba_number = models.CharField(max_length=35, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.employee:
            self.full_name = f"{self.employee.first_name} {self.employee.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} {self.title}"

    class Meta:
        verbose_name = "BankAccount"
        verbose_name_plural = "BankAccount"
        ordering = ("-created_at",)




