#nosql models for users browser history and wishlist

from mongoengine import Document, StringField, IntField, DateTimeField, ListField, ReferenceField
from datetime import datetime, timezone
from nosql_products.models_nosql import Product

class BrowsingHistory(Document):
    user_id = StringField(required=True)
    product = ReferenceField(Product, required=True)
    viewed_at = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection' : 'browsing_history',
        'ordering' : ['-viewed_at']
        }

class Wishlist(Document):
    user_id = StringField(required=True,unique=True) # one wishlist per user
    product_ids = ListField(ReferenceField(Product))

    meta = {
        'collection' : 'wishlists'
        }