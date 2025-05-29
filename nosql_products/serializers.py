# nosql_products/serializers.py

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from bson import ObjectId

from .models_nosql import Category, Product


class ObjectIdField(serializers.CharField):
    """
    Field to handle MongoDB ObjectId fields in DRF serializers.
    """
    def to_internal_value(self, data):
        if not ObjectId.is_valid(data):
            raise ValidationError("Invalid ObjectId format")
        return ObjectId(data)

    def to_representation(self, value):
        return str(value)


class CategorySerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)


class ProductSerializer(serializers.Serializer):
    id             = ObjectIdField(read_only=True)
    owner          = serializers.CharField(read_only=True)
    name           = serializers.CharField()
    description    = serializers.CharField(allow_blank=True, required=False)
    price          = serializers.FloatField()
    stock          = serializers.IntegerField()
    category       = ObjectIdField()
    images         = serializers.ListField(child=serializers.URLField(), default=list)
    tags           = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    available      = serializers.BooleanField(default=True)
    specifications = serializers.DictField(child=serializers.CharField(), required=False, default=dict)
    created_at     = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # 1) Get the logged-in user
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise ValidationError({"owner": "User must be authenticated."})
        user_id = str(request.user.id)

        # 2) Resolve and remove category ObjectId
        category_oid = validated_data.pop('category', None)
        if category_oid is None:
            raise ValidationError({"category": "Category is required."})
        try:
            category = Category.objects.get(id=category_oid)
        except Category.DoesNotExist:
            raise ValidationError({"category": "Invalid category reference."})

        # 3) Build & save Product
        product = Product(
            owner=user_id,
            category=category,
            **validated_data
        )
        product.save()
        return product

    def update(self, instance, validated_data):
        # Update allowed fields
        for field in ['name', 'description', 'price', 'stock', 'available', 'tags', 'specifications', 'images']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        # Handle category change
        if 'category' in validated_data:
            instance.category = Category.objects.get(id=validated_data['category'])
        instance.save()
        return instance

