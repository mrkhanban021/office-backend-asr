import tempfile
from rest_framework.response import Response
from  rest_framework import status
from .serializers import (ToolsSerializers, EmployeeSerializers, ToolTransferLogSerializers, PeopleCategorySerializers,
                          ExternalPersonSerializers, EntryExitLogSerializers, DepartmentSerializers, ToolCategorySerializers)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import (Tools, Employee, ToolTransferLog, PeopleCategory, ExternalPerson, EntryExitLog, Department, ToolCategory)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import HttpResponse, FileResponse
from weasyprint import HTML
from django.template.loader import render_to_string
import pandas as pd
import io



class ToolsApiList(ListCreateAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializers
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToolsApiListDetail(RetrieveUpdateDestroyAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializers



class ToolTransferLogList(ListCreateAPIView):
    queryset = ToolTransferLog.objects.all()
    serializer_class = ToolTransferLogSerializers
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToolTransferLogDetail(RetrieveUpdateDestroyAPIView):
    queryset = ToolTransferLog.objects.all()
    serializer_class = ToolTransferLogSerializers


class EmployeeList(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializers
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployeeListDetail(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializers


class PeopleCategoryList(ListCreateAPIView):
    queryset = PeopleCategory.objects.all()
    serializer_class = PeopleCategorySerializers


class PeopleCategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = PeopleCategory.objects.all()
    serializer_class = PeopleCategorySerializers


class ExternalPersonList(ListCreateAPIView):
    queryset = ExternalPerson.objects.all()
    serializer_class = ExternalPersonSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExternalPersonDetail(RetrieveUpdateDestroyAPIView):
    queryset = ExternalPerson.objects.all()
    serializer_class = ExternalPersonSerializers


class EntryExitLogList(ListCreateAPIView):
    queryset = EntryExitLog.objects.all()
    serializer_class = EntryExitLogSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EntryExitLogDetail(RetrieveUpdateDestroyAPIView):
    queryset = EntryExitLog.objects.all()
    serializer_class = EntryExitLogSerializers


class DepartmentList(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class DepartmentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers



class ToolCategoryList(ListCreateAPIView):
    queryset = ToolCategory.objects.all()
    serializer_class = ToolCategorySerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToolCategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = ToolCategory.objects.all()
    serializer_class = ToolCategorySerializers



class ExportEmployeeList(APIView):

    def get(self, request):
        data = Employee.objects.all().values(
            'first_name',
            'last_name',
            'department__title',
            'phone_number',
            'email',
            'hire_date',
            'position',
            'address',
            'date_of_birth',
            'id_code',
            'is_active'
        )

        df = pd.DataFrame(list(data))

        date_fields = ['hire_date', 'date_of_birth']
        for field in date_fields:
            if field in df.columns:
                df[field] = df[field].apply(lambda x: str(x) if x else '')

        df['is_active'] = df['is_active'].apply(lambda x: 'فعال' if x else 'غیرفعال')

        df.rename(columns={
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'department__title': 'بخش',
            'phone_number': 'شماره تماس',
            'hire_date': 'تاریخ استخدام',
            'position': 'موقعیت شغلی',
            'address': 'ادرس',
            'date_of_birth': 'تاریخ تولد',
            'id_code': 'کدملی',
            'is_active': 'وضعیت فعال بودن'
        }, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Employees')

            workbook = writer.book
            worksheet = writer.sheets['Employees']

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
        filename = "employees.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response



class ExportToolsExcel(APIView):

    def get(self, request):
        # دریافت اطلاعات از مدل Tools
        data = Tools.objects.select_related('ToolCategory', 'department').all().values(
            'title',
            'ToolCategory__title',
            'department__title',
            'seria_number',
            'counting',
            'description',
        )

        df = pd.DataFrame(list(data))

        # تغییر نام ستون‌ها برای زیبایی
        df.rename(columns={
            'title': 'نام ابزار',
            'ToolCategory__title': 'دسته‌بندی',
            'department__title': 'دپارتمان',
            'seria_number': 'شماره سریال',
            'counting': 'تعداد',
            'description': 'توضیحات',
        }, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Tools')

            workbook = writer.book
            worksheet = writer.sheets['Tools']

            header_format = workbook.add_format({
                'bold': False,
                'text_wrap': True,
                'valign': 'center',
                'fg_color': '#FFFF00',
                'border': 1
            })

            for col_num, column in enumerate(df.columns):
                worksheet.write(0, col_num, column, header_format)
                column_len = max(df[column].astype(str).map(len).max(), len(column))
                worksheet.set_column(col_num, col_num, column_len + 2)

        output.seek(0)
        filename = "tools.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response



class ExportToolTransferLog(APIView):

    def get(self, request):
        data = ToolTransferLog.objects.all().values(
            'tool__title',
            'employee__first_name',
            'employee__last_name',
            'taken_at',
            'returned_at',
            'notes',
        )

        df = pd.DataFrame(list(data))

        for date_field in ['taken_at', 'returned_at']:
            if date_field in df.columns:
                df[date_field] = df[date_field].apply(lambda x: str(x) if x else '')


        if 'employee__first_name' in df.columns and 'employee__last_name' in df.columns:
            df['اسم پرسنل'] = df['employee__first_name'].fillna('') + ' ' + df['employee__last_name'].fillna('')
            df.drop(['employee__first_name', 'employee__last_name'], axis=1, inplace=True)


        df.rename(columns={
            'tool__title': 'اسم ابزار',
            'taken_at': 'تاریخ تحویل',
            'returned_at': 'تاریخ بازگشت',
            'notes': 'یادداشت‌ها',
        }, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='tool_transfer')

            workbook = writer.book
            worksheet = writer.sheets['tool_transfer']

            header_format = workbook.add_format({
                'bold': False,
                'text_wrap': True,
                'valign': 'center',
                'fg_color': '#FFFF00',
                'border': 1
            })

            for col_num, column in enumerate(df.columns):
                worksheet.write(0, col_num, column, header_format)
                column_len = max(df[column].astype(str).map(len).max(), len(column))
                worksheet.set_column(col_num, col_num, column_len + 2)

        output.seek(0)
        return HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="tool_transfer_log.xlsx"'}
        )


class ExportEntryExitLog(APIView):

    def format_jdatetime_or_time(self, x):
        import jdatetime
        if not x:
            return ''
        try:
            if isinstance(x, jdatetime.datetime) or isinstance(x, jdatetime.date):
                return x.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(x, (str,)):
                return x
            else:
                # معمولاً entry_time که تایم هست
                return x.strftime('%H:%M:%S')
        except Exception:
            return str(x)

    def get(self, request):
        data = EntryExitLog.objects.all().values(
            'employee__first_name',
            'employee__last_name',
            'exit_time',
            'entry_time',
            'reason',
        )

        df = pd.DataFrame(list(data))

        if 'exit_time' in df.columns:
            df['exit_time'] = df['exit_time'].apply(self.format_jdatetime_or_time)

        if 'entry_time' in df.columns:
            df['entry_time'] = df['entry_time'].apply(self.format_jdatetime_or_time)

        if 'employee__first_name' in df.columns and 'employee__last_name' in df.columns:
            df['نام پرسنل'] = df['employee__first_name'].fillna('') + ' ' + df['employee__last_name'].fillna('')
            df.drop(['employee__first_name', 'employee__last_name'], axis=1, inplace=True)

        df.rename(columns={
            'exit_time': 'زمان خروج',
            'entry_time': 'زمان ورود',
            'reason': 'دلیل',
        }, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='entry_exit_log')

            workbook = writer.book
            worksheet = writer.sheets['entry_exit_log']

            header_format = workbook.add_format({
                'bold': False,
                'text_wrap': True,
                'valign': 'center',
                'fg_color': '#FFFF00',
                'border': 1
            })

            for col_num, column in enumerate(df.columns):
                worksheet.write(0, col_num, column, header_format)
                column_len = max(df[column].astype(str).map(len).max(), len(column))
                worksheet.set_column(col_num, col_num, column_len + 2)

        output.seek(0)
        return HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="entry_exit_log.xlsx"'}
        )


class ExportExternalPerson(APIView):


    def format_jdate(self, x):
        import jdatetime
        if not x:
            return ''
        try:
            # اگر datetime جلالی است، تاریخ و زمان را به صورت 'YYYY-MM-DD HH:mm:ss' برگردان
            if isinstance(x, jdatetime.datetime):
                return x.strftime('%Y-%m-%d %H:%M:%S')
            # اگر فقط تاریخ جلالی است، فقط تاریخ را برگردان
            elif isinstance(x, jdatetime.date):
                return x.strftime('%Y-%m-%d')
            else:
                return str(x)
        except Exception:
            return str(x)

    def get(self, request):
        data = ExternalPerson.objects.all().values(
            'category__title',
            'full_name',
            'national_code',
            'phone_number',
            'compony',
            'centered_at',
            'exit',
            'notex',
        )

        df = pd.DataFrame(list(data))

        # تبدیل فیلدهای تاریخ جلالی به رشته
        for date_field in ['centered_at', 'exit']:
            if date_field in df.columns:
                df[date_field] = df[date_field].apply(self.format_jdate)

        df.rename(columns={
            'category__title': 'دسته‌بندی',
            'full_name': 'نام کامل',
            'national_code': 'کد ملی',
            'phone_number': 'شماره تلفن',
            'compony': 'شرکت',
            'centered_at': 'تاریخ ورود',
            'exit': 'تاریخ خروج',
            'notex': 'توضیحات',
        }, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='ExternalPersons')

            workbook = writer.book
            worksheet = writer.sheets['ExternalPersons']

            header_format = workbook.add_format({
                'bold': False,
                'text_wrap': True,
                'valign': 'center',
                'fg_color': '#FFFF00',
                'border': 1
            })

            for col_num, column in enumerate(df.columns):
                worksheet.write(0, col_num, column, header_format)
                column_len = max(df[column].astype(str).map(len).max(), len(column))
                worksheet.set_column(col_num, col_num, column_len + 2)

        output.seek(0)
        return HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="external_persons.xlsx"'}
        )


class EnttryexitLogToPDF(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            data = EntryExitLog.objects.get(pk=pk)
        except EntryExitLog.DoesNotExist:
            return Response({'error': 'کاربری یافت نشد'}, status=status.HTTP_404_NOT_FOUND )

        html_string = render_to_string("EnttryexitLog/EnttryexitLogToPDF.html", {"data": data})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True, filename=f'{data.employee.first_name} {data.employee.last_name}.pdf')



class ToolTransferLogToPDF(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            data = ToolTransferLog.objects.get(pk=pk)
        except EntryExitLog.DoesNotExist:
            return Response({'error': 'کاربری یافت نشد'},status=status.HTTP_404_NOT_FOUND )

        html_string = render_to_string("EnttryexitLog/ToolTransferLog.html", {"data": data})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True, filename=f'{data.employee.first_name} {data.employee.last_name}.pdf')


class ExternalPersonPDF(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            data = ExternalPerson.objects.get(pk=pk)
        except EntryExitLog.DoesNotExist:
            return Response({'error': 'کاربری یافت نشد'},status=status.HTTP_404_NOT_FOUND )

        html_string = render_to_string("EnttryexitLog/visitor_entry.html", {"data": data})
        html = HTML(string=html_string)
        result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=result.name)

        result.seek(0)
        return FileResponse(result, as_attachment=True, filename=f'{data.full_name} {data.compony}.pdf')


