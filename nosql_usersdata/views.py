#views for users browser history and wishlist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from mongoengine import DoesNotExist, ValidationError

from .models_nosql import BrowsingHistory, Wishlist
from nosql_products.models_nosql import Product
from .serializers import BrowsingHistorySerializer, WishlistSerializer

# BrowsingHistory ViewSet
class BrowsingHistoryViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"message": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        history = BrowsingHistory.objects(user_id=user_id)
        serializer = BrowsingHistorySerializer(history, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        
        if not user_id or not product_id:
            return Response({"message": "user_id and product_id are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
            browsing_history = BrowsingHistory(user_id=user_id, product=product)
            browsing_history.save()
            serializer = BrowsingHistorySerializer(browsing_history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class WishlistViewSet(viewsets.ViewSet):
    def list(self, request):
        """List all wishlists or filter by user_id."""
        user_id = request.query_params.get('user_id')
        if user_id:
            wishlists = Wishlist.objects.filter(user_id=user_id)
        else:
            wishlists = Wishlist.objects.all()

        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a specific wishlist by user_id."""
        try:
            wishlist = Wishlist.objects.get(user_id=pk)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        except Wishlist.DoesNotExist:
            return Response({"message": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"])
    def add_product(self, request, pk=None):
        """Add a product to a specific wishlist."""
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"message": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wishlist = Wishlist.objects.get(user_id=pk)
            product = Product.objects.get(id=product_id)

            # Add the product to the wishlist if it's not already present
            if product not in wishlist.products.all():
                wishlist.products.add(product)
                wishlist.save()
                return Response({"message": "Product added to wishlist."})
            else:
                return Response({"message": "Product already in wishlist."})

        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Wishlist.DoesNotExist:
            return Response({"message": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def remove_product(self, request, pk=None):
        """Remove a product from a specific wishlist."""
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"message": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wishlist = Wishlist.objects.get(user_id=pk)
            product = Product.objects.get(id=product_id)

            # Remove the product if it exists in the wishlist
            if product in wishlist.products.all():
                wishlist.products.remove(product)
                wishlist.save()
                return Response({"message": "Product removed from wishlist."})
            else:
                return Response({"message": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)

        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Wishlist.DoesNotExist:
            return Response({"message": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)