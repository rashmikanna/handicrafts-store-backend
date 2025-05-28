import requests
import re
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

# ✅ Import password validation
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def verify_recaptcha(recaptcha_response):
    secret_key = settings.RECAPTCHA_SECRET_KEY
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    return result.get('success', False)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    # Validate required fields
    if not username or not password or not email:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Validate password using Django validators (including your custom one)
    try:
        validate_password(password)
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.is_active = False
    user.save()

    # Send verification email
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    activation_link = f"http://localhost:3000/verify/{uid}/{token}/"

    subject = 'Verify your email'
    message = render_to_string('email_verification.html', {
        'user': user,
        'activation_link': activation_link,
    })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    

    return Response({
        'message': 'User created. Please check your email to verify your account.'
    }, status=status.HTTP_201_CREATED)

    recaptcha_token = request.data.get('recaptcha')

    if not recaptcha_token:
        return Response({'error': 'reCAPTCHA token is missing'}, status=status.HTTP_400_BAD_REQUEST)

    recaptcha_response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': '6LcBT00rAAAAALk3UBYksLsKMGxJsLXLf2zHONKy',  # 🗝️ Replace with your secret key
            'response': recaptcha_token
        }
    )

    result = recaptcha_response.json()
    if not result.get('success'):
        return Response({'error': 'reCAPTCHA verification failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully. You can now log in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Account is already activated.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Activation link is invalid or has expired!'}, status=status.HTTP_400_BAD_REQUEST)
