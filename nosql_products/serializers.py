#serializers for nosql_products, categories

from rest_framework import serializers
from .models_nosql import Category, Product
from bson import ObjectId

class ObjectIdField(serializers.CharField):
    def to_representation(self, value):
        return str(value) if isinstance(value, ObjectId) else super().to_representation(value)

class CategorySerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)

class ProductSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    owner = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    category = serializers.CharField(allow_blank=True, required=False) 
    images = serializers.ListField(child=serializers.URLField(), required=False, allow_empty=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    available = serializers.BooleanField(default=True)
    specifications = serializers.DictField(child=serializers.CharField(), required=False)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data, **kwargs):
         # owner will be injected by view.perform_create(serializer.save(owner=...))
         owner = kwargs.get('owner', None)
         if owner is None:
             raise ValidationError({"owner": "No owner provided"})
 
         # Resolve category from its ID string
         cat_id = validated_data.pop('category', None)
         if cat_id:
             from .models_nosql import Category
             validated_data['category'] = Category.objects.get(id=ObjectId(cat_id))
         return Product(owner=owner, **validated_data).save()


    def update(self, instance, validated_data):
        # only allow owner, name, description, price, stock, etc.
        for attr, value in validated_data.items():
            if attr == 'category' and value:
                from .models_nosql import Category
                setattr(instance, 'category', Category.objects.get(id=ObjectId(value)))
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
