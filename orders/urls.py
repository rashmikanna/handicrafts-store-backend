from django.urls import path
from .views import (
    CreateOrderView,
    OrderDetailView,
    UserOrderHistoryView,
    create_stripe_session,
    create_razorpay_order,  # ✅ NEW
)

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('history/', UserOrderHistoryView.as_view(), name='order-history'),
    path('create-stripe-session/', create_stripe_session, name='stripe-session'),
    path('create-razorpay-order/', create_razorpay_order, name='razorpay-order'),  # ✅ NEW
]
