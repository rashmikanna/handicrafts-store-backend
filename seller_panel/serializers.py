#serializers for seller panel

from rest_framework import serializers
from .models import SellerProfile

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model   = SellerProfile
        exclude = ['id', 'user', 'approved', 'applied_at']

class SellerStatusSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        if obj is None:
            return 'none'
        return 'approved' if obj.approved else 'pending'
