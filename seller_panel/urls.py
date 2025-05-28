#urls for seller_panel

from django.urls import path, include
from .views import seller_status, seller_signup, seller_products


app_name = 'seller_panel'
urlpatterns = [
    path('signup/', seller_signup, name='seller_signup'),
    path('status/', seller_status, name='seller_status'),
    path('products/', seller_products, name='seller_products'),
]


