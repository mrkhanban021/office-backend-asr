from django.contrib import admin
from .models import LogingLog, Department, Employee, ToolCategory, Tools, ToolTransferLog, EntryExitLog, ExternalPerson, PeopleCategory


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "created_time", "user")
    list_display_links = ("id", "title", "user")
    list_editable = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ("created_time",)
    fieldsets = (
        ("information", {
            "fields": ("title", "is_active", "created_time", "user")
        }),
    )


class LogingLogAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "user", "login_time")
    search_fields = ("full_name", "user")
    list_display_links = ("id", "full_name", "user", "login_time")
    list_per_page = 13


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "position", "id_code", "department", "is_active")
    list_display_links = ("id", "last_name", "position", "id_code", "department")
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 13

    fieldsets = (
        ("Personal information", {
            "fields": ("first_name", "last_name", "id_code", "address", "date_of_birth", "phone_number", "email", "signature_image", "fingerprint_image")
        }),
        ("Job information", {
            "fields": ("department", "hire_date", "position", "created_at", "updated_at", "user")
        }),
    )


class ToolCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "updated_at", "user")
    list_display_links = ("title", "user")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 13
    fieldsets = (
        ("information", {
            "fields": ("title", "is_active", "updated_at", "created_at", "user")
        }),
    )


class ToolsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "seria_number", "counting", "updated_at", "department", "ToolCategory")
    list_display_links = ("id", "title", "seria_number")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("information", {
            "fields": ("ToolCategory", "title", "seria_number", "counting", "description", "created_at", "updated_at", "user",
                       "department")
        }),
    )


class ToolTransferLogAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "tool", "taken_at", "user", "returned_at")
    list_display_links = ("id", "employee", "tool", "taken_at", "user", "returned_at")
    list_filter = ("employee", "tool", "user")
    search_fields = ("employee", "tool", "taken_at", "user", "returned_at")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 13
    fieldsets = (
        ("information", {
            "fields": ("employee", "tool", "taken_at", "user", "returned_at", "notes", "created_at", "updated_at")
        }),
    )


class EntryExitLogAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "exit_time", "entry_time", "user", "created_at")
    list_display_links = ("employee", "entry_time", "user", "created_at")
    list_filter = ("employee", "entry_time", "user")
    readonly_fields = ("created_at", "updated_at", "exit_time")
    list_per_page = 13

    fieldsets = (
        ("information", {
            "fields": ("employee", "exit_time", "entry_time", "reason", "user", "created_at", "updated_at")
        }),
    )


class PeopleCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    list_display_links = ("id", "title", "created_at")
    search_fields = ("id", "title",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 13

    fieldsets = (
        ("information", {
            "fields": ("title","is_active", "created_at", "updated_at")
        }),
    )


class ExternalPersonAdmin(admin.ModelAdmin):
    list_display = ('id', "full_name", "national_code", "phone_number", "compony", "category")
    list_display_links = ("id", "full_name")
    list_filter = ("category", "centered_at")
    search_fields = ("full_name", "national_code", "phone_number")
    readonly_fields = ("centered_at", )
    list_per_page = 13

    fieldsets = (
        ("information", {
            "fields": ("category", "full_name", "national_code", "phone_number", "compony", "centered_at", "exit", "notex", "user")
        }),
    )


admin.site.register(Tools, ToolsAdmin)
admin.site.register(ToolCategory, ToolCategoryAdmin)
admin.site.register(LogingLog, LogingLogAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(ToolTransferLog, ToolTransferLogAdmin)
admin.site.register(EntryExitLog, EntryExitLogAdmin)
admin.site.register(PeopleCategory, PeopleCategoryAdmin)
admin.site.register(ExternalPerson, ExternalPersonAdmin)
