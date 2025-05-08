from django.contrib import admin
from .models import AssistanceRequest, MonthlyAssistanceSummary, BankAccount


@admin.register(AssistanceRequest)
class AssistanceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "request_date", "amount", "loan_installment", "installment_amount", "total_installments", "paid_installments", "manager_approval", "admin_approval", "ceo_approval", "final_approval")
    list_filter = ("final_approval", "manager_approval", "admin_approval", "ceo_approval")
    search_fields = ("full_name", "employee")
    list_display_links = ("id", "employee", "request_date")
    readonly_fields = ("request_date", "create_at", "updated_at")

    fieldsets = (
        ("information", {
            "fields": ("employee", "full_name", "request_date", "amount", "fingerprint_image", "loan_installment", "installment_amount", "total_installments", "paid_installments", "account_number", "card_number", "sheba_number", "explanation", "manager_approval", "admin_approval", "ceo_approval", "final_approval", "create_at", "updated_at")
        }),
    )


@admin.register(MonthlyAssistanceSummary)
class MonthlyAssistanceSummaryAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "year", "month", "total_assistance")
    list_filter = ("month", "year", "total_assistance")
    search_fields = ("full_name", "employee", "month")
    list_display_links = ("id", "employee", "year", "month", "total_assistance")


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "title", "account_number", "card_number", "sheba_number")
    list_filter = ("title",)
    search_fields = ("employee", "full_name", "card_number", "account_number", "sheba_number")
    list_display_links = ("id", "employee", "title", "account_number", "card_number", "sheba_number")
