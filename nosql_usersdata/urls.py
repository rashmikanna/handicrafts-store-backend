#urls for users browser history and wishlist

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrowsingHistoryViewSet, WishlistViewSet

router = DefaultRouter()
router.register(r'browsinghistory', BrowsingHistoryViewSet, basename='browsinghistory')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('api/users/', include(router.urls)),
    # Explicitly add custom actions for the WishlistViewSet
    path('api/users/wishlist/<str:pk>/add_product/', WishlistViewSet.as_view({'post': 'add_product'}), name='wishlist-add-product'),
    path('api/users/wishlist/<str:pk>/remove_product/', WishlistViewSet.as_view({'post': 'remove_product'}), name='wishlist-remove-product'),
]
