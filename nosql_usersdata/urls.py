# nosql_usersdata/urls.py

from django.urls import path
from .views import get_user_wishlist, WishlistViewSet

# Map the two action routes (no user_id in URL; JWT tells us who)
wishlist_add    = WishlistViewSet.as_view({'post': 'add_product'})
wishlist_remove = WishlistViewSet.as_view({'post': 'remove_product'})

urlpatterns = [
    # GET: full product list for current user
    path('wishlist/', get_user_wishlist, name='get_user_wishlist'),

    # POST: add/remove
    path('wishlist/add_product/',    wishlist_add,    name='wishlist_add_product'),
    path('wishlist/remove_product/', wishlist_remove, name='wishlist_remove_product'),
]
