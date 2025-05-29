# seller_panel/admin.py

from django.contrib import admin
from .models import SellerProfile
from django.utils.html import format_html

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user','shop_name','approved','applied_at', 'view_id_document')
    list_filter  = ('approved','craft_category','district')
    actions = ['approve_sellers']

    def view_id_document(self, obj):
        if obj.id_document:
            return format_html('<a href="{}" target="_blank">View Document</a>', obj.id_document.url)
        return "No document"
    view_id_document.short_description = "ID Document"

    def approve_sellers(self, request, qs):
        qs.update(approved=True)
    approve_sellers.short_description = "Approve selected artisans"
