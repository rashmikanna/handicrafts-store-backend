# nosql_products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    upload_image,
    ProductListView,
    my_seller_products,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', upload_image, name='upload_image'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('seller/products/', my_seller_products, name='my-seller-products'),
]
