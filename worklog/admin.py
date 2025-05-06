from django.contrib import admin
from .models import LogingLog, Department, Employee, ToolCategory, Tools


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "created_time", "created_by")
    list_display_links = ("id", "title", "created_by")
    list_editable = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ("created_time",)
    fieldsets = (
        ("information", {
            "fields": ("title", "is_active", "created_time", "created_by")
        }),
    )


class LogingLogAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "user", "login_time")
    search_fields = ("full_name", "user")
    list_display_links = ("id", "full_name", "user", "login_time")


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "position", "employee_id", "department", "is_active")
    list_display_links = ("id", "last_name", "position", "employee_id", "department")
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Personal information", {
            "fields": ("first_name", "last_name", "address", "date_of_birth", "phone_number", "email")
        }),
        ("Job information", {
            "fields": ("department", "hire_date", "position", "employee_id", "created_at", "updated_at", "created_by"),
            "classes": ("collapse",)
        })
    )


class ToolCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "updated_at", "created_by")
    list_display_links = ("title", "created_by")
    readonly_fields = ("created_at", "updated_at")
    fieldsets  = (
        ("information", {
            "fields": ("title", "updated_at", "created_at", "created_by")
        }),
    )


class ToolsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "seria_number", "updated_at", "department", "ToolCategory")
    list_display_links = ("id", "title", "seria_number")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("information", {
            "fields": ("ToolCategory", "title", "seria_number", "description", "created_at", "updated_at", "created_by",
                       "department")
        }),
    )


admin.site.register(Tools, ToolsAdmin)
admin.site.register(ToolCategory, ToolCategoryAdmin)
admin.site.register(LogingLog, LogingLogAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
