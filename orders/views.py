from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from nosql_products.models_nosql import Product  # Adjust if you renamed it
from django.contrib.auth.models import User

class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        # Let DRF handle the saving logic
        response = super().create(request, *args, **kwargs)

        # Log what is being returned to the client
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
    
class SellerOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller_id = str(request.user.id)

        # Step 1: Get product IDs owned by the current seller from MongoDB
        seller_products = Product.objects(owner=seller_id).only('id')
        seller_product_ids = set(str(p.id) for p in seller_products)

        # Step 2: Get OrderItems where product_id is in seller's products
        seller_items = OrderItem.objects.filter(product_id__in=seller_product_ids)

        # Step 3: Get related orders from those items
        order_ids = set(item.order_id for item in seller_items)
        orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')

        # Step 4: Build response manually (filtered to seller’s items only)
        data = []
        for order in orders:
            items = seller_items.filter(order=order)
            data.append({
                "order_id": order.id,
                "buyer_id": order.user.id,
                "placed_on": order.created_at,
                "status": order.status,
                "total_price": order.total_price,
                "shipping_address": order.shipping_address,
                "payment_method": order.payment_method,
                "items": [
                    {
                        "product_name": item.product_name,
                        "quantity": item.quantity,
                        "price": item.price,
                        "image": item.image,
                    }
                    for item in items
                ]
            })

        return Response(data)