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



class AllLeaveRequestsPDFView(APIView):

    def get(self, request):
        leaves = LeaveRequest.objects.filter(final_approval=True).order_by('-created_at')

        if not leaves.exists():
            return Response({"error": "هیچ درخواست تایید شده ای یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        html_string = render_to_string('pdfLeaveRequest/all_leave_requests.html', {'leaves': leaves})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True, filename="all_leave_requests.pdf")



class Assistance_requestPDF(APIView):

    def get(self, request, pk):
        try:
            assistance = AssistanceRequest.objects.get(pk=pk, final_approval=True)
        except AssistanceRequest.DoesNotExist:
            return Response({'error': "درخواست به تایید نهایی نرسیده است"}, status=status.HTTP_400_BAD_REQUEST)

        html_string = render_to_string("assistanceRequest/single_assistance_request.html", {"assistance": assistance})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True , filename=f"{assistance.full_name}_assistance.pdf")



class AllAssistanceRequestsPDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        assistances = AssistanceRequest.objects.filter(final_approval=True).order_by('created_at')

        if not assistances.exists():
            return Response({"error":"هیچ درخواست تایید شده ای یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        html_string = render_to_string("assistanceRequest/all_assistance_requests.html", {"assistances": assistances})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True, filename="all_assistance_requests.pdf")


