# seller_panel/views.py

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    parser_classes
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as drf_status

from .models import SellerProfile
from .serializers import SellerProfileSerializer, SellerStatusSerializer

from accounts.models import Profile

# Import your NoSQL Product model + serializer
from nosql_products.models_nosql import Product
from nosql_products.serializers import ProductSerializer


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def seller_signup(request):
    """
    POST /api/seller/signup/
    Creates a SellerProfile for the authenticated user.
    """
    user = request.user

    # Prevent duplicate applications
    if SellerProfile.objects.filter(user=user).exists():
        return Response(
            {'detail': 'You have already applied to sell.'},
            status=drf_status.HTTP_400_BAD_REQUEST
        )

    # Validate incoming data
    serializer = SellerProfileSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    # Update user role in Profile
    try:
        prof = Profile.objects.get(user=user)
        prof.role = 'producer'
        prof.save()
    except Profile.DoesNotExist:
        return Response(
            {'detail': 'User profile not found.'},
            status=drf_status.HTTP_400_BAD_REQUEST
        )

    # Save new SellerProfile
    serializer.save(user=user)

    return Response(
        {'detail': 'Seller application submitted, pending approval.'},
        status=drf_status.HTTP_201_CREATED
    )


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def seller_status(request):
    """
    GET /api/seller/status/
    Returns the approval status of the authenticated user's seller application.
    Response: { "approved": true/false }
    """
    try:
        sp = SellerProfile.objects.get(user=request.user)
    except SellerProfile.DoesNotExist:
        return Response(
            {'detail': 'No seller application found.'},
            status=drf_status.HTTP_404_NOT_FOUND
        )

    data = SellerStatusSerializer(sp).data
    return Response(data, status=drf_status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def seller_products(request):
    """
    GET /api/seller/products/
    Lists all products where `owner` matches request.user.id (as string).
    """
    user_id = str(request.user.id)
    qs = Product.objects.filter(owner=user_id)
    serializer = ProductSerializer(qs, many=True)
    return Response(serializer.data, status=drf_status.HTTP_200_OK)
