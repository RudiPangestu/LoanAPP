from django.contrib import admin
from .models import LoanApplication

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_id','no_of_dependents','education', 'self_employed','income_annum','loan_amount', 'loan_term','cibil_score','residential_assets_value','commercial_assets_value', 'luxury_assets_value','bank_asset_value','is_approved', 'created_at')
    list_filter = ('is_approved', 'education', 'self_employed')
    search_fields = ('application_id',)
    readonly_fields = ('application_id', 'created_at', 'is_approved')