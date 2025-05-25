from django.contrib import admin
from .models import AssistanceRequest, MonthlyAssistanceSummary, BankAccount, LeaveRequest, MonthlyLeaveSummary


@admin.register(AssistanceRequest)
class AssistanceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "request_date", "amount", "loan_installment", "installment_amount", "total_installments", "paid_installments", "manager_approval", "admin_approval", "ceo_approval", "final_approval")
    list_filter = ("final_approval", "manager_approval", "admin_approval", "ceo_approval")
    search_fields = ("full_name", "employee")
    list_display_links = ("id", "employee", "request_date")
    readonly_fields = ("request_date", "created_at", "updated_at")
    list_per_page = 13


@admin.register(MonthlyAssistanceSummary)
class MonthlyAssistanceSummaryAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "year", "month", "total_assistance", "assistance_requests_count")
    list_filter = ("month", "year", "total_assistance")
    search_fields = ("full_name", "employee", "month")
    list_display_links = ("id", "employee", "year", "month", "total_assistance")
    list_per_page = 13


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "title", "account_number", "card_number", "sheba_number", "is_active")
    list_filter = ("title", "is_active")
    search_fields = ("employee", "full_name", "card_number", "account_number", "sheba_number")
    list_display_links = ("id", "employee", "title", "account_number", "card_number", "sheba_number")
    list_per_page = 13


class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'leave_type', 'duration_type', 'request_date', 'manager_approval', 'final_approval')
    list_display_links = ('id', 'full_name', 'leave_type', 'duration_type')
    list_filter = ('leave_type', 'duration_type', 'manager_approval', 'admin_approval', 'ceo_approval', 'final_approval')
    search_fields = ('full_name', 'leave_type', 'duration_type')
    list_per_page = 13
    date_hierarchy = 'request_date'


class MonthlyLeaveSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'year', 'month', 'total_leave', 'leave_requests_count', 'create_at')
    list_display_links = ('id', 'full_name', 'year', 'month', 'total_leave', 'leave_requests_count', 'create_at')
    search_fields = ('employee__first_name', 'employee__last_name')
    list_filter = ('year', 'month')
    list_per_page = 13


admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(MonthlyLeaveSummary, MonthlyLeaveSummaryAdmin)
