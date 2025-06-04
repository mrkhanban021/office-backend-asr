import jdatetime
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
import pandas as pd
import decimal
import io
from datetime import datetime, date, time


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
        return FileResponse(result, as_attachment=True, filename=f"{assistance.full_name}_assistance.pdf")


class AllAssistanceRequestsPDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        assistances = AssistanceRequest.objects.filter(final_approval=True).order_by('created_at')

        if not assistances.exists():
            return Response({"error": "هیچ درخواست تایید شده ای یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        html_string = render_to_string("assistanceRequest/all_assistance_requests.html", {"assistances": assistances})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True, filename="all_assistance_requests.pdf")


class ExportAssistanceExcelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = AssistanceRequest.objects.all().values(
            'full_name',
            'request_date',
            'amount',
            'loan_installment',
            'installment_amount',
            'total_installments',
            'paid_installments',
            'manager_approval',
            'admin_approval',
            'ceo_approval',
            'final_approval',
        )

        df = pd.DataFrame(list(data))


        if 'request_date' in df.columns:
            df['request_date'] = df['request_date'].apply(lambda x: str(x) if x else '')

        numeric_fields = ['amount', 'installment_amount', 'total_installments', 'paid_installments']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: float(x) if isinstance(x, (int, float, decimal.Decimal)) else None
                )

        df.rename(columns={
            'full_name': 'نام کامل',
            'request_date': 'تاریخ درخواست',
            'amount': 'مقدار',
            'loan_installment': 'اقساط وام',
            'installment_amount': 'مبلغ هر قسط',
            'total_installments': 'کل اقساط',
            'paid_installments': 'اقساط پرداخت شده',
            'manager_approval': 'تایید مدیر',
            'admin_approval': 'تایید ادمین',
            'ceo_approval': 'تایید مدیرعامل',
            'final_approval': 'تایید نهایی',
        }, inplace=True)

        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Assistance')

        workbook = writer.book
        worksheet = writer.sheets['Assistance']

        header_format = workbook.add_format({
            'bold': False,
            'text_wrap': False,
            'valign': 'vcenter',
            'fg_color': '#FFFF00',
            'border': 1
        })
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        cell_format = workbook.add_format({'border': 1})

        for col_num, column in enumerate(df.columns):
            worksheet.write(0, col_num, column, header_format)
            column_len = max(df[column].astype(str).map(len).max(), len(column))
            worksheet.set_column(col_num, col_num, column_len + 2)

            # اگر ستون عددی بود، فرمت عدد بده
            if column in numeric_fields:
                worksheet.set_column(col_num, col_num, column_len + 2, number_format)



        writer.close()
        output.seek(0)

        filename = f"assistance_requests_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class ExportMonthlyAssistanceSummaryExcelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = MonthlyAssistanceSummary.objects.all().values(
            'full_name',
            'year',
            'month',
            'total_assistance',
            'assistance_requests_count',
        )

        df = pd.DataFrame(list(data))

        numeric_fields = ['total_assistance']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: float(x) if isinstance(x, (int, float, decimal.Decimal)) else None
                )

        df.rename(columns={
            'full_name': 'نام کامل',
            'year': 'سال',
            'month': 'ماه',
            'total_assistance': 'جمع کل',
            'assistance_requests_count': 'تعداد درخواست‌ها',
        }, inplace=True)

        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, index=False, sheet_name="MonthlyAssist")

        workbook = writer.book
        worksheet = writer.sheets['MonthlyAssist']

        header_format = workbook.add_format({
            'bold': False,
            'text_wrap': False,
            'valign': 'vcenter',
            'fg_color': '#FFFF00',
            'border': 1
        })

        number_format = workbook.add_format({'num_format': '#,##0.00'})
        cell_format = workbook.add_format({'border': 1})

        for col_num, column in enumerate(df.columns):
            worksheet.write(0, col_num, column, header_format)
            column_len = max(df[column].astype(str).map(len).max(), len(column))
            worksheet.set_column(col_num, col_num, column_len + 2)

            if column in numeric_fields:
                worksheet.set_column(col_num, col_num, column_len + 2, number_format)

        for row_num, row_data in enumerate(df.values, start=1):
            for col_num, cell_value in enumerate(row_data):
                worksheet.write(row_num, col_num, cell_value, cell_format)

        writer.close()
        output.seek(0)

        filename = f"monthly_summary_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response



class ExportLeaveRequestExcel(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        leave_requests = LeaveRequest.objects.all()

        data = []
        for leave in leave_requests:
            data.append({
                'نام کامل': leave.full_name,
                'تاریخ درخواست': str(leave.request_date) if leave.request_date else '',
                'نوع مرخصی': leave.get_leave_type_display() if leave.leave_type else '',
                'نوع مدت': leave.get_duration_type_display() if leave.duration_type else '',
                'تاریخ ساعتی': str(leave.hourly_date) if leave.hourly_date else '',
                'از ساعت': str(leave.time_from) if leave.time_from else '',
                'تا ساعت': str(leave.time_to) if leave.time_to else '',
                'تاریخ شروع': str(leave.start_date) if leave.start_date else '',
                'تاریخ پایان': str(leave.end_date) if leave.end_date else '',
            })

        df = pd.DataFrame(list(data))

        # تابع تبدیل همه تاریخ‌ها و زمان‌ها به رشته قابل فهم برای اکسل
        def convert_to_string(val):
            if isinstance(val, (datetime, date)):
                return val.strftime('%Y-%m-%d')
            if isinstance(val, jdatetime.date):
                return val.strftime('%Y-%m-%d')
            if isinstance(val, time):
                return val.strftime('%H:%M')
            return ""

        date_fields = ['request_date', 'hourly_date', 'start_date', 'end_date', 'time_from', 'time_to']
        for field in date_fields:
            if field in df.columns:
                df[field] = df[field].apply(convert_to_string)

        df.rename(columns={
            'full_name': 'نام کامل',
            'request_date': 'تاریخ درخواست',
            'leave_type': 'نوع مرخصی',
            'duration_type': 'نوع مدت',
            'hourly_date': 'تاریخ ساعتی',
            'time_from': 'از ساعت',
            'time_to': 'تا ساعت',
            'start_date': 'تاریخ شروع',
            'end_date': 'تاریخ پایان',
        }, inplace=True)

        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, index=False, sheet_name="LeaveRequests")

        workbook = writer.book
        worksheet = writer.sheets['LeaveRequests']

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'vcenter',
            'fg_color': '#FFFF00',
            'border': 1
        })

        cell_format = workbook.add_format({'border': 1})

        for col_num, column in enumerate(df.columns):
            worksheet.write(0, col_num, column, header_format)
            column_len = max(df[column].astype(str).map(len).max(), len(column))
            worksheet.set_column(col_num, col_num, column_len + 2)

        for row_num, row_data in enumerate(df.values, start=1):
            for col_num, cell_value in enumerate(row_data):
                worksheet.write(row_num, col_num, cell_value, cell_format)

        writer.close()
        output.seek(0)

        filename = f"leave_requests_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response



class ExportMonthlyLeaveSummaryExcelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = MonthlyLeaveSummary.objects.all().values(
            'full_name',
            'year',
            'month',
            'total_leave',
            'leave_requests_count',
        )

        df = pd.DataFrame(list(data))

        # اطمینان از اینکه total_leave عددی است
        numeric_fields = ['total_leave']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = df[field].apply(
                    lambda x: float(x) if isinstance(x, (int, float, decimal.Decimal)) else None
                )
        df.rename(columns={
            'full_name': 'نام کامل',
            'year': 'سال',
            'month': 'ماه',
            'total_leave': 'مجموع مرخصی (ساعت)',
            'leave_requests_count': 'تعداد درخواست‌ها',
        }, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="MonthlyLeave")

            workbook = writer.book
            worksheet = writer.sheets['MonthlyLeave']

            header_format = workbook.add_format({
                'bold': False,
                'text_wrap': False,
                'valign': 'vcenter',
                'fg_color': '#FFFF00',
                'border': 1
            })

            number_format = workbook.add_format({'num_format': '#,##0.00'})  # نمایش اعشار

            for col_num, column in enumerate(df.columns):
                worksheet.write(0, col_num, column, header_format)

                column_len = max(df[column].astype(str).map(len).max(), len(column))
                worksheet.set_column(col_num, col_num, column_len + 2)

                if column in numeric_fields:
                    worksheet.set_column(col_num, col_num, None, number_format)

            # worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

        output.seek(0)
        filename = "monthly_leave_summary.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class ExportBankAccountExcelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = BankAccount.objects.all().values(
            'full_name',
            'title',
            'account_number',
            'card_number',
            'sheba_number',
            'is_active',
        )

        df = pd.DataFrame(list(data))

        df['is_active'] = df['is_active'].apply(lambda x: 'فعال' if x else 'غیرفعال')


        df.rename(columns={
            'full_name': 'نام و نام خانوادگی',
            'title': "نام بانک",
            'account_number': 'شماره حساب' ,
            'card_number': 'شماره کارت',
            'sheba_number': 'شماره شبا',
            'is_active': 'وضعیت حساب'
        },inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="BankAccounts")

            workbook = writer.book
            worksheet = writer.sheets['BankAccounts']

            header_format = workbook.add_format({
                'bold': False,
                'text_wrap': False,
                'valign': 'vcenter',
                'fg_color': '#FFFF00',
                'border': 1
            })

            for col_num, column in enumerate(df.columns):
                worksheet.write(0, col_num, column, header_format)
                column_len = max(df[column].astype(str).map(len).max(), len(column))
                worksheet.set_column(col_num, col_num, column_len + 2)

            # worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

        output.seek(0)
        filename = "bank_accounts.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


