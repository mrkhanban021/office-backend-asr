from django.urls import path
from .views import ToolsApiList, ToolsApiListDetail
app_name = "worklog"

urlpatterns = [
    path("toolslist/", ToolsApiList.as_view()),
    path("toolslist/<int:pk>", ToolsApiListDetail.as_view())
]
