#serializers for nosql_products, categories

from rest_framework import serializers
from .models_nosql import Category, Product
from bson import ObjectId

#custom serializer field to handle ObjectId
class ObjectIdField(serializers.CharField):
    def to_representation(self, value):
        #convert ObjectId to string
        if isinstance(value, ObjectId):
            return str(value)
        return super().to_representation(value)

class CategorySerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True) 
    name = serializers.CharField()
    description = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True) 
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    category = CategorySerializer()
    images = serializers.ListField(child=serializers.URLField(),required=False,allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(),required=False,allow_null=True)
    available = serializers.BooleanField()
    specifications = serializers.DictField(child=serializers.CharField(), required=False)
    created_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = str(instance.category.id) if instance.category else None
        return rep