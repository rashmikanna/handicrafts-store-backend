#serializers for users browser history and wishlist

from rest_framework import serializers
from .models_nosql import BrowsingHistory, Wishlist
from nosql_products.serializers import ProductSerializer
from bson import ObjectId

#custom serializer field to handle ObjectId
class ObjectIdField(serializers.CharField):
    def to_representation(self, value):
        #convert ObjectId to string
        if isinstance(value, ObjectId):
            return str(value)
        return super().to_representation(value)

class BrowsingHistorySerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    user_id = ObjectIdField()
    product = ProductSerializer()
    viewed_at = serializers.DateTimeField()


class WishlistSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    user_id = ObjectIdField()
    product_ids = serializers.ListField(
        child=ObjectIdField(),
        required=False
    )


