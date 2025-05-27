from django.urls import path
from .views import (AssistanceRequestList, AssistanceRequestDetails, MonthlyAssistanceSummaryList,
                    MonthlyAssistanceSummaryDetail, BankAccountList, BankAccountDetails,
                    LeaveRequestList, LeaveRequestDetail, MonthlyLeaveSummaryList, MonthlyLeaveSummaryDetail
                    , LeaveRequestPDFView)

app_name = "human_resources"

urlpatterns = [
    path("AssistanceRequest/", AssistanceRequestList.as_view(), name="AssistanceRequestList"),
    path("AssistanceRequest/<int:pk>", AssistanceRequestDetails.as_view(), name="AssistanceRequestDetails"),
    path("MonthlyAssistance/", MonthlyAssistanceSummaryList.as_view(), name="MonthlyAssistanceSummaryList"),
    path("MonthlyAssistance/<int:pk>", MonthlyAssistanceSummaryDetail.as_view(), name="MonthlyAssistanceSummaryDetail"),
    path("BankAccount/", BankAccountList.as_view(), name="BankAccountList"),
    path("BankAccount/<int:pk>", BankAccountDetails.as_view(), name="BankAccountDetails"),
    path("LeaveRequest/", LeaveRequestList.as_view(), name="LeaveRequestList"),
    path("LeaveRequest/<int:pk>", LeaveRequestDetail.as_view(), name="LeaveRequestDetail"),
    path("MonthlyLeave/", MonthlyLeaveSummaryList.as_view(), name="MonthlyLeaveSummaryList"),
    path("MonthlyLeave/<int:pk>", MonthlyLeaveSummaryDetail.as_view(), name="MonthlyLeaveSummaryDetail"),
    path('leave-request/<int:pk>/pdf/', LeaveRequestPDFView.as_view(), name='leave-request-pdf'),

]

