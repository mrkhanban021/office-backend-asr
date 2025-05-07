from django.urls import path
from .views import (ToolsApiList, ToolsApiListDetail, EmployeeList, EmployeeListDetail,
                    ToolTransferLogList, ToolTransferLogDetail, PeopleCategoryList, PeopleCategoryDetail,
                    ExternalPersonList, ExternalPersonDetail, EntryExitLogList, EntryExitLogDetail, DepartmentList, DepartmentDetail,
                    ToolCategoryList, ToolCategoryDetail)
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

]
