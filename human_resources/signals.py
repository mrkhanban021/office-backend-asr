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





def has_leave_amount_changed(old, new):
    if old.duration_type != new.duration_type:
        return True

    if old.duration_type == "daily":
        return old.start_date != new.start_date or old.end_date != new.end_date

    if old.duration_type == "hourly":
        return (
            old.hourly_date != new.hourly_date or
            old.time_from != new.time_from or
            old.time_to != new.time_to
        )

    return False




@receiver(pre_save, sender=LeaveRequest)
def check_final_approval_change(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)

        if old_instance.final_approval and instance.final_approval:
            # بررسی تغییر مقدار در درخواست تأییدشده
            if has_leave_amount_changed(old_instance, instance):
                MonthlyLeaveSummary.update_summary(
                    employee=instance.employee,
                    leave_request=instance,
                    old_request=old_instance
                )

        elif not old_instance.final_approval and instance.final_approval:
            # تأیید جدید
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
