from rest_framework import serializers
from .models import AssistanceRequest, MonthlyAssistanceSummary, BankAccount, LeaveRequest, MonthlyLeaveSummary
from django_jalali.serializers.serializerfield import JDateField, jDateTimeFieldModel


class AssistanceRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = AssistanceRequest
        fields = "__all__"


class MonthlyAssistanceSummarySerializers(serializers.ModelSerializer):
    class Meta:
        model = MonthlyAssistanceSummary
        fields = "__all__"


class BankAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = "__all__"


class LeaveRequestSerializers(serializers.ModelSerializer):
    hourly_date = JDateField(required=False, allow_null=True)
    start_date = JDateField(required=False, allow_null=True)
    end_date = JDateField(required=False, allow_null=True)

    class Meta:
        model = LeaveRequest
        fields = ("employee", "full_name", "request_date", "leave_type", "duration_type", "hourly_date", "time_from", "time_to", "start_date", "end_date",
                  "manager_approval", "manager_comment", "admin_approval", "ceo_approval", "ceo_reject_reason", "final_approval", "created_at", "updated_at")


class MonthlyLeaveSummarySerializers(serializers.ModelSerializer):
    class Meta:
        model = MonthlyLeaveSummary
        fields = "__all__"


