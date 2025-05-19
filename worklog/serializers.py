from rest_framework import serializers
from .models import (Department, Employee, ToolCategory, Tools, PeopleCategory, ToolTransferLog, ExternalPerson, EntryExitLog)
from django.contrib.auth import get_user_model
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField

USER = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = USER
        fields = ("id", "full_name")

    def get_full_name(self, obj):
        if hasattr(obj, "profile"):
            return f"{obj.profile.name} {obj.profile.last_name}"


class ToolCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ToolCategory
        exclude = ["created_at", "updated_at"]


class DepartmentSerializers(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Department
        fields = ("id", "title", "is_active", "user",)


class EmployeeSerializers(serializers.ModelSerializer):
    department_id = DepartmentSerializers(source="department", read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    date_of_birth = JDateField()
    hire_date = JDateField()


    user = SimpleUserSerializer(read_only=True)


    class Meta:
        model = Employee
        fields = ("id", "first_name", "last_name", "employee_id", "email", "phone_number", "hire_date",
                  "position", "signature_image", "fingerprint_image", "address", "is_active", "date_of_birth", "user", "department", "department_id")


class EmployeeSerializersName(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ("id", "full_name")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ToolsSerializers(serializers.ModelSerializer):
    created_by_display = SimpleUserSerializer(source="created_by", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())
    ToolCategory = serializers.PrimaryKeyRelatedField(queryset=ToolCategory.objects.all())
    ToolCategory_list = ToolCategorySerializers(source="ToolCategory", read_only=True)
    department_list = DepartmentSerializers(source="department", read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Tools
        fields = ("id","title", "seria_number", "counting", "description", "created_at", "created_by_display", "created_by",
                  "ToolCategory_list", "ToolCategory", "department_list", "department")


class ToolsSerializersName(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = ("id", "title", "ToolCategory", "department")


class ToolTransferLogSerializers(serializers.ModelSerializer):
    tool_name = ToolsSerializersName(source="tool", read_only=True)
    tool = serializers.PrimaryKeyRelatedField(queryset=Tools.objects.all())
    employee_name =  EmployeeSerializersName(source="employee" , read_only=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = ToolTransferLog
        fields = ("id", "employee","employee_name", "taken_at", "returned_at", "registering_user", "notes", "created_at", "tool","tool_name")


class PeopleCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = PeopleCategory
        fields = ("id", "title", "description",)
        read_only_fields = ("created_at", "updated_at")


class ExternalPersonSerializers(serializers.ModelSerializer):
    category_name = PeopleCategorySerializers(source="category", read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=PeopleCategory.objects.all())
    register_user_name = SimpleUserSerializer(source="register_user", read_only=True)
    register_user = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())

    class Meta:
        model = ExternalPerson
        fields = ("id", "full_name", "national_code", "phone_number", "compony","notex","entered_at",
                  "register_user","register_user_name", "category_name", "category", "category_name")
        read_only_fields = ("entered_at", "updated_at")


class EntryExitLogSerializers(serializers.ModelSerializer):
    employee_name = EmployeeSerializersName(source="employee", read_only=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    approved_name = SimpleUserSerializer(source="approved_by", read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())

    class Meta:
        model = EntryExitLog
        fields = ("id", "employee", "employee_name", "exit_time","entry_time", "reason", "approved_by", "approved_name")
        read_only_fields = ("created_at", "updated_at", "exit_time")