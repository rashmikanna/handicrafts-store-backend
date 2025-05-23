# seller_panel/views.py

from django.views.decorators.csrf import csrf_exempt
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
from rest_framework import status

from seller_panel.models import SellerProfile
from accounts.models import Profile

@csrf_exempt
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def seller_signup(request):
    # —— DEBUG (feel free to remove once happy) ——
    print("---- AUTHED seller_signup called ----")
    print("HTTP_AUTHORIZATION:", request.headers.get('Authorization'))
    print("request.auth:", request.auth)
    print("request.user:", request.user)

    user = request.user

    # Prevent duplicate applications
    if SellerProfile.objects.filter(user=user).exists():
        return Response(
            {'detail': 'You have already applied to sell.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Required seller fields
    required = [
        'shop_name', 'craft_category',
        'district', 'village',
        'govt_id_type', 'govt_id_number',
        'bank_account_no', 'bank_ifsc'
    ]
    data = request.data

    # Check text fields
    missing = [f for f in required if not data.get(f)]
    if missing:
        return Response(
            {'detail': f'Missing fields: {", ".join(missing)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check file upload
    id_doc = request.FILES.get('id_document')
    if not id_doc:
        return Response(
            {'detail': 'id_document file is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update user role in Profile
    try:
        prof = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return Response(
            {'detail': 'User profile not found.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    prof.role = 'producer'
    prof.save()

    # Create the SellerProfile
    seller_data = {f: data[f] for f in required}
    seller_data['id_document'] = id_doc
    SellerProfile.objects.create(user=user, **seller_data)

    return Response(
        {'detail': 'Seller application submitted, pending approval.'},
        status=status.HTTP_201_CREATED
    )
