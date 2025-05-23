# seller_panel/admin.py

from django.contrib import admin
from .models import SellerProfile

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user','shop_name','approved','applied_at')
    list_filter  = ('approved','craft_category','district')
    actions = ['approve_sellers']

    def approve_sellers(self, request, qs):
        qs.update(approved=True)
    approve_sellers.short_description = "Approve selected artisans"
