from rest_framework import serializers
from .models_nosql import Wishlist

class WishlistSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    products = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Wishlist
        fields = ['user_id', 'products']