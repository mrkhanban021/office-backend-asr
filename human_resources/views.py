import tempfile

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from weasyprint import HTML
from .models import (AssistanceRequest, MonthlyAssistanceSummary, BankAccount, MonthlyLeaveSummary, LeaveRequest)
from .serializers import (AssistanceRequestSerializers, MonthlyAssistanceSummarySerializers, BankAccountSerializers,
                          LeaveRequestSerializers, MonthlyLeaveSummarySerializers)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.http import HttpResponse, FileResponse
import tempfile


class AssistanceRequestList(ListCreateAPIView):
    queryset = AssistanceRequest.objects.all()
    serializer_class = AssistanceRequestSerializers


class AssistanceRequestDetails(RetrieveUpdateDestroyAPIView):
    queryset = AssistanceRequest.objects.all()
    serializer_class = AssistanceRequestSerializers


class MonthlyAssistanceSummaryList(ListCreateAPIView):
    queryset = MonthlyAssistanceSummary.objects.all()
    serializer_class = MonthlyAssistanceSummarySerializers


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


class LeaveRequestPDFView(APIView):

    def get(self, request, pk):
        try:
            leave = LeaveRequest.objects.get(pk=pk, final_approval=True)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "درخواست به تایید نهایی نرسیده است"}, status=status.HTTP_404_NOT_FOUND)

        html_string = render_to_string('pdfLeaveRequest/single_leave_request.html', {'leave': leave})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True, filename=f'{leave.full_name}_leave.pdf')