from django.contrib import admin
from .models import Partner, PromoCode


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user',
                    'phone', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['company_name', 'user__username', 'user__email']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'partner',
                    'discount_percent', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'discount_percent']
    search_fields = ['code', 'partner__company_name']
