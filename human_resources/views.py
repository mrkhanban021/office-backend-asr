from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import (AssistanceRequest, MonthlyAssistanceSummary, BankAccount, MonthlyLeaveSummary, LeaveRequest)
from .serializers import (AssistanceRequestSerializers, MonthlyAssistanceSummarySerializers, BankAccountSerializers,
                          LeaveRequestSerializers, MonthlyLeaveSummarySerializers)
from rest_framework.permissions import AllowAny



class AssistanceRequestList(ListCreateAPIView):
    queryset = AssistanceRequest.objects.all()
    serializer_class = AssistanceRequestSerializers
    permission_classes = [AllowAny]


class AssistanceRequestDetails(RetrieveUpdateDestroyAPIView):
    queryset = AssistanceRequest.objects.all()
    serializer_class = AssistanceRequestSerializers
    permission_classes = [AllowAny]


class MonthlyAssistanceSummaryList(ListCreateAPIView):
    queryset = MonthlyAssistanceSummary.objects.all()
    serializer_class = MonthlyAssistanceSummarySerializers
    permission_classes = [AllowAny]


class MonthlyAssistanceSummaryDetail(RetrieveUpdateDestroyAPIView):
    queryset = MonthlyAssistanceSummary.objects.all()
    serializer_class = MonthlyAssistanceSummarySerializers
    permission_classes = [AllowAny]


class BankAccountList(ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializers
    permission_classes = [AllowAny]


class BankAccountDetails(RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializers
    permission_classes = [AllowAny]


class LeaveRequestList(ListCreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializers
    permission_classes = [AllowAny]


class LeaveRequestDetail(RetrieveUpdateDestroyAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializers
    permission_classes = [AllowAny]


class MonthlyLeaveSummaryList(ListCreateAPIView):
    queryset = MonthlyLeaveSummary.objects.all()
    serializer_class = MonthlyLeaveSummarySerializers
    permission_classes = [AllowAny]


class MonthlyLeaveSummaryDetail(RetrieveUpdateDestroyAPIView):
    queryset = MonthlyLeaveSummary.objects.all()
    serializer_class = MonthlyLeaveSummarySerializers
    permission_classes = [AllowAny]
