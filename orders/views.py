from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer

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