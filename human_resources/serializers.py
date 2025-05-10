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

    class Meta:
        model = LeaveRequest
        exclude = []


class MonthlyLeaveSummarySerializers(serializers.ModelSerializer):
    class Meta:
        model = MonthlyLeaveSummary
        fields = "__all__"


