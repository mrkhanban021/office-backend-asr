from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import AssistanceRequest, MonthlyAssistanceSummary, LeaveRequest, MonthlyLeaveSummary


@receiver(pre_save, sender=AssistanceRequest)
def check_final_approval_change_or_amount_update(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)

        # فقط اگر درخواست نهایی تأیید شده بود
        if old_instance.final_approval:
            # بررسی اینکه آیا مبلغ تغییر کرده؟
            if old_instance.amount != instance.amount:
                difference = instance.amount - old_instance.amount
                MonthlyAssistanceSummary.update_summary_amount_change(
                    employee=instance.employee,
                    amount_diff=difference,
                    date=old_instance.created_at  # تاریخ اولیه درخواست
                )

        # بررسی تغییر وضعیت final_approval
        if old_instance.final_approval != instance.final_approval:
            if instance.final_approval:
                # تازه تأیید شده
                MonthlyAssistanceSummary.update_summary(
                    instance.employee, instance.amount, date=instance.created_at
                )

    except sender.DoesNotExist:
        # اولین بار ثبت شده
        if instance.final_approval:
            MonthlyAssistanceSummary.update_summary(
                instance.employee, instance.amount, date=instance.created_at
            )


@receiver(pre_save, sender=LeaveRequest)
def check_final_approval_change(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.final_approval != instance.final_approval:
            if instance.final_approval:
                MonthlyLeaveSummary.update_summary(
                    employee=instance.employee,
                    leave_request=instance
                )
    except sender.DoesNotExist:
        if instance.final_approval:
            MonthlyLeaveSummary.update_summary(
                employee=instance.employee,
                leave_request=instance
            )


