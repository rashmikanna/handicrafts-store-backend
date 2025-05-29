from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    role = serializers.CharField(source='profile.role', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

class SignupSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        # Validate email format
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Check uniqueness
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role', 'consumer')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_active = False  # Deactivate account until email confirmed
        user.set_password(password)
        user.save()
        # Create profile with role
        Profile.objects.create(user=user, role=role)
        return user
