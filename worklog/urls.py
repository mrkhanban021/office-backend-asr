from django.urls import path
from .views import (ToolsApiList, ToolsApiListDetail, EmployeeList, EmployeeListDetail,
                    ToolTransferLogList, ToolTransferLogDetail, PeopleCategoryList, PeopleCategoryDetail,
                    ExternalPersonList, ExternalPersonDetail, EntryExitLogList, EntryExitLogDetail, DepartmentList, DepartmentDetail,
                    ToolCategoryList, ToolCategoryDetail, ExportEmployeeList, ExportToolsExcel, ExportToolTransferLog, ExportEntryExitLog,
                    ExportExternalPerson, EnttryexitLogToPDF, ToolTransferLogToPDF, ExternalPersonPDF)
app_name = "worklog"

urlpatterns = [
    path("toolslist/", ToolsApiList.as_view()),
    path("toolslist/<int:pk>", ToolsApiListDetail.as_view()),
    path("tooltransferlog/", ToolTransferLogList.as_view()),
    path("tooltransferlog/<int:pk>", ToolTransferLogDetail.as_view()),
    path("peoplecategory/", PeopleCategoryList.as_view()),
    path("peoplecategory/<int:pk>", PeopleCategoryDetail.as_view()),
    path("externalperson/", ExternalPersonList.as_view()),
    path("externalperson/<int:pk>", ExternalPersonDetail.as_view()),
    path("employeelist/", EmployeeList.as_view()),
    path("employeelist/<int:pk>", EmployeeListDetail.as_view()),
    path("entryexitlog/", EntryExitLogList.as_view()),
    path("entryexitlog/<int:pk>", EntryExitLogDetail.as_view()),
    path("department/", DepartmentList.as_view()),
    path("department/<int:pk>", DepartmentDetail.as_view()),
    path("toolcategory/", ToolCategoryList.as_view()),
    path("toolcategory/<int:pk>", ToolCategoryDetail.as_view()),
    path("ExportEmployeeList/", ExportEmployeeList.as_view()),
    path("ExportToolsExcel/", ExportToolsExcel.as_view()),
    path("ExportToolTransferLog/", ExportToolTransferLog.as_view()),
    path("ExportEntryExitLog/", ExportEntryExitLog.as_view()),
    path("ExportExternalPerson/", ExportExternalPerson.as_view()),
    path("EnttryexitLogToPDF/<int:pk>/pdf", EnttryexitLogToPDF.as_view()),
    path("ToolTransferLogToPDF/<int:pk>/pdf", ToolTransferLogToPDF.as_view()),
    path("ExternalPersonPDF/<int:pk>/pdf", ExternalPersonPDF.as_view()),

]
