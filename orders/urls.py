from django.urls import path
from .views import CreateOrderView, OrderDetailView, UserOrderHistoryView, SellerOrderListView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path("history/", UserOrderHistoryView.as_view(), name="order-history"),
    path('seller/', SellerOrderListView.as_view(), name='seller-orders'),
]
