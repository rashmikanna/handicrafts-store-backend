# reviews/urls.py
from django.urls import path
from .views import ProductReviews

urlpatterns = [
    path('<str:product_id>/reviews/', ProductReviews.as_view(), name='product-reviews'),
]
