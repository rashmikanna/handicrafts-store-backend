# nosql_usersdata/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import (
    action, api_view, authentication_classes, permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from mongoengine.errors import DoesNotExist

from .models_nosql import Wishlist
from nosql_products.models_nosql import Product
from .serializers import WishlistSerializer
from nosql_products.serializers import ProductSerializer


class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        user_id = str(request.user.id)
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'message': 'product_id is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Manual get_or_create for Wishlist
        wishlist = Wishlist.objects(user_id=user_id).first()
        if not wishlist:
            wishlist = Wishlist(user_id=user_id, products=[])
        
        # Add product
        try:
            product = Product.objects.get(id=product_id)
        except DoesNotExist:
            return Response({'message': 'Product not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        if product not in wishlist.products:
            wishlist.products.append(product)
            wishlist.save()

        return Response({'message': 'Product added to wishlist.'})

    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        user_id = str(request.user.id)
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'message': 'product_id is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        wishlist = Wishlist.objects(user_id=user_id).first()
        if not wishlist:
            return Response({'message': 'Wishlist not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            product = Product.objects.get(id=product_id)
        except DoesNotExist:
            return Response({'message': 'Product not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        if product in wishlist.products:
            wishlist.products.remove(product)
            wishlist.save()

        return Response({'message': 'Product removed from wishlist.'})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_wishlist(request):
    """
    Returns an array of full Product objects in the logged-in user's wishlist.
    """
    user_id = str(request.user.id)

    wishlist = Wishlist.objects(user_id=user_id).first()
    if not wishlist:
        # If none exists, return empty list
        return Response([])

    # Serialize full Product documents
    products = list(wishlist.products)
    serialized = ProductSerializer(products, many=True)
    return Response(serialized.data)
