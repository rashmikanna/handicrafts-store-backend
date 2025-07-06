import stripe
import uuid
import requests
import razorpay  # ✅ NEW
from django.conf import settings
from django.shortcuts import render
<<<<<<< HEAD
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
=======
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Order
>>>>>>> 6659e3c (WIP: Final updates before switching to main)
from .serializers import OrderSerializer
from nosql_products.models_nosql import Product  # Adjust if you renamed it
from django.contrib.auth.models import User

# Stripe Setup
stripe.api_key = settings.STRIPE_SECRET_KEY

# ✅ Razorpay Setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        payment_method = data.get("payment_method")

        # Simulate payment for UPI or Card
        if payment_method in ["UPI", "Card"]:
            try:
                result = {
                    "status": "success",
                    "transaction_id": "txn_mock_" + str(uuid.uuid4().hex[:10])
                }

                if result.get("status") != "success":
                    return Response({"message": "❌ Payment Failed"}, status=status.HTTP_400_BAD_REQUEST)

                print("✅ Simulated transaction ID:", result.get("transaction_id"))

            except Exception as e:
                print("❌ Payment simulation error:", str(e))
                return Response({"message": "Payment Gateway Error"}, status=status.HTTP_502_BAD_GATEWAY)

        response = super().create(request, *args, **kwargs)
        print("🚀 Order creation response:", response.data)
        return response


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_stripe_session(request):
    cart_items = request.data.get("items", [])
    user = request.user

    line_items = [
        {
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item['product_name'],
                },
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        } for item in cart_items
    ]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:3000/checkout?success=true',
            cancel_url='http://localhost:3000/checkout',
            metadata={'user_id': user.id},
        )
        return Response({'id': session.id})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# ✅ Razorpay Order Creation API
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_razorpay_order(request):
    try:
        total_price = request.data.get("total_price")
        amount = int(float(total_price) * 100)  # Convert to paise

        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,
        })

        return Response({
            "order_id": razorpay_order['id'],
            "amount": razorpay_order['amount'],
            "currency": razorpay_order['currency'],
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)
