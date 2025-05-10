from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import AssistanceRequest, MonthlyAssistanceSummary, LeaveRequest, MonthlyLeaveSummary


@receiver(pre_save, sender=AssistanceRequest)
def check_final_approval_change(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.final_approval != instance.final_approval:
            if instance.final_approval:
                MonthlyAssistanceSummary.update_summary(instance.employee, instance.amount)
    except sender.DoesNotExist:
        if instance.final_approval:
            MonthlyAssistanceSummary.update_summary(instance.employee, instance.amount)


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


