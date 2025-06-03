from .serializers import (ToolsSerializers, EmployeeSerializers, ToolTransferLogSerializers, PeopleCategorySerializers,
                          ExternalPersonSerializers, EntryExitLogSerializers, DepartmentSerializers, ToolCategorySerializers)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from .models import (Tools, Employee, ToolTransferLog, PeopleCategory, ExternalPerson, EntryExitLog, Department, ToolCategory)


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
    permission_classes = (AllowAny,)


class EmployeeList(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializers
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployeeListDetail(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializers
    permission_classes = (AllowAny,)


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
