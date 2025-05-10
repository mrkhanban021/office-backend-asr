from django.db import models
from worklog.models import Employee
from django.utils import timezone
from django.contrib.auth import get_user_model
import jdatetime
from datetime import datetime
from django_jalali.db import models as jmodels
from decimal import Decimal

USER = get_user_model()


class AssistanceRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    request_date = jmodels.jDateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    loan_installment = models.BooleanField(default=False)
    installment_amount = models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=2)  # مبلغ قسط
    total_installments = models.PositiveIntegerField(null=True, blank=True)  # تعداد کل اقساط
    paid_installments = models.PositiveIntegerField(default=0)  # چند قسط پرداخت شده
    account_number = models.CharField(max_length=30, blank=True, null=True)  # شماره حساب (در صورت نیاز)
    card_number = models.CharField(max_length=30, blank=True, null=True)  # شماره کارت
    sheba_number = models.CharField(max_length=35, null=True, blank=True)  # شماره شبا
    explanation = models.TextField(null=True, blank=True)  # توضیحات درباره دلیل درخواست مساعده

    manager_approval = models.BooleanField(default=False)
    manager_comment = models.TextField(null=True, blank=True)
    admin_approval = models.BooleanField(default=False)
    ceo_approval = models.BooleanField(default=False)
    ceo_comment = models.TextField(null=True, blank=True)

    final_approval = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.employee:
            self.full_name = f'{self.employee.first_name} {self.employee.last_name}'
        if self.manager_approval and self.admin_approval and self.ceo_approval:
            self.final_approval = True
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
    assistance_requests_count = models.PositiveIntegerField(default=0)
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
        summary.assistance_requests_count += 1
        summary.save()

    class Meta:
        verbose_name = "MonthlyAssistanceSummary"
        verbose_name_plural = "MonthlyAssistanceSummary"
        ordering = ("-create_at",)


class BankAccount(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(null=True, blank=True, max_length=100)
    title = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.CharField(max_length=30, null=True, blank=True)
    card_number = models.CharField(max_length=30, null=True, blank=True)
    sheba_number = models.CharField(max_length=35, null=True, blank=True)
    is_active = models.BooleanField(default=True)

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


class LeaveRequest(models.Model):
    class LeaveType(models.TextChoices):
        ENTITLEMENT = "entitlement", "استحقاقی"
        ILLNESS = "illness", "استعلاجی"
        WITHOUT_PAY = "without_pay", "بدون حقوق"

    class DurationType(models.TextChoices):
        HOURLY = "hourly", "ساعتی"
        DAILY = "daily", "روزانه"

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    request_date = jmodels.jDateField(auto_now_add=True)

    leave_type = models.CharField(max_length=20, choices=LeaveType.choices, null=True, blank=True)
    duration_type = models.CharField(max_length=20, choices=DurationType.choices, null=True, blank=True)

    hourly_date = jmodels.jDateField(null=True, blank=True)
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)

    start_date = jmodels.jDateField(null=True, blank=True)
    end_date = jmodels.jDateField(null=True, blank=True)

    manager_approval = models.BooleanField(default=False)
    manager_comment = models.TextField(null=True, blank=True)
    admin_approval = models.BooleanField(default=False)
    ceo_approval = models. BooleanField(default=False)
    ceo_reject_reason = models.TextField(null=True, blank=True)

    final_approval = models.BooleanField(default=False)

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.employee:
            self.full_name = f'{self.employee.first_name} {self.employee.last_name}'
        if self.manager_approval and self.admin_approval and self.ceo_approval:
            self.final_approval = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} {self.request_date}"

    class Meta:
        verbose_name = "LeaveRequest"
        verbose_name_plural = "LeaveRequests"
        ordering = ("-request_date",)


class MonthlyLeaveSummary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    total_leave = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    leave_requests_count = models.PositiveIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.employee:
            self.full_name = f'{self.employee.first_name} {self.employee.last_name}'
        super().save(*args, **kwargs)

    @staticmethod
    def update_summary(employee, leave_request):
        now = timezone.now()
        shamsi_date = jdatetime.date.fromgregorian(year=now.year, month=now.month, day=now.day)
        shamsi_year = shamsi_date.year
        shamsi_month = shamsi_date.month

        if leave_request.duration_type == "daily":

            days_off = (leave_request.end_date - leave_request.start_date).days + 1
            amount = days_off * 8
        elif leave_request.duration_type == "hourly":

            j_date = jdatetime.date(leave_request.hourly_date.year, leave_request.hourly_date.month,
                                    leave_request.hourly_date.day)
            gregorian_date = j_date.togregorian()
            start_time = datetime.combine(gregorian_date, leave_request.time_from)
            end_time = datetime.combine(gregorian_date, leave_request.time_to)
            amount = (end_time - start_time).seconds / 3600
            amount = Decimal(amount)

        summary, created = MonthlyLeaveSummary.objects.get_or_create(
            employee=employee, year=shamsi_year, month=shamsi_month
        )
        summary.total_leave += amount
        summary.leave_requests_count += 1
        summary.save()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "MonthlyLeaveSummary"
        verbose_name_plural = "MonthlyLeaveSummaries"
        ordering = ("-create_at",)


