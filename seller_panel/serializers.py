from rest_framework import serializers
from .models import SellerProfile

class SellerProfileSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = SellerProfile
        fields = [
            'shop_name',
            'craft_category',
            'district',
            'village',
            'govt_id_type',
            'govt_id_number',
            'id_document',
            'bank_account_no',
            'bank_ifsc',
        ]


class SellerStatusSerializer(serializers.ModelSerializer):
    """
    Used for GET /seller/status/
    """
    class Meta:
        model = SellerProfile
        fields = ['approved']
