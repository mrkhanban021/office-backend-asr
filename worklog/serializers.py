from rest_framework import serializers
from .models import (Department, Employee, LogingLog, ToolCategory, Tools)
from django.contrib.auth import get_user_model

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
        fields = ("id", "title")


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "title", "is_active")


class ToolsSerializers(serializers.ModelSerializer):
    created_by_display = SimpleUserSerializer(source="created_by", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=USER.objects.all())
    ToolCategory = serializers.PrimaryKeyRelatedField(queryset=ToolCategory.objects.all())
    ToolCategory_list = ToolCategorySerializers(source="ToolCategory", read_only=True)
    department_list = DepartmentSerializers(source="department", read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Tools
        fields = ("title", "seria_number", "description", "created_at", "created_by_display", "created_by",
                  "ToolCategory_list", "ToolCategory", "department_list", "department")
