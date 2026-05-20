from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import CustomUser


# ================================
# Register Serializer
# ================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser

        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'password2'
        ]

    def validate_email(self, value):

        email = value.lower()

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        return email

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop('password2')

        password = validated_data.pop('password')

        user = CustomUser(**validated_data)

        user.set_password(password)

        user.save()

        return user


# ================================
# Login Serializer
# ================================

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials"
            )

        attrs['user'] = user

        return attrs


# ================================
# User Profile Serializer
# ================================

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'profile_picture',
            'bio',
            'is_online',
            'last_seen',
            'phone',
        ]

        read_only_fields = [
            'id',
            'email',
            'is_online',
            'last_seen',
        ]