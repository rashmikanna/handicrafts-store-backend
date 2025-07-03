from mongoengine import Document, StringField, ListField, ReferenceField
from nosql_products.models_nosql import Product

class Wishlist(Document):
    user_id = StringField(required=True, unique=True)
    products = ListField(ReferenceField(Product))
    meta = {'collection': 'wishlists'}