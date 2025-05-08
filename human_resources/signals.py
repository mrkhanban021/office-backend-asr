from django.db.models.signals import  pre_save
from django.dispatch import receiver
from .models import AssistanceRequest, MonthlyAssistanceSummary


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