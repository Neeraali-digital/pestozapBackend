"""
Serializers for the users app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import UserProfile

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for user creation.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'password'
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    class Meta:
        model = UserProfile
        fields = (
            'bio', 'website', 'company', 'location',
            'email_notifications', 'sms_notifications', 'marketing_emails'
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.
    """
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'address', 'date_of_birth', 'profile_picture',
            'is_verified', 'full_name', 'profile', 'date_joined'
        )
        read_only_fields = ('id', 'is_verified', 'date_joined')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    """
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'phone_number',
            'address', 'date_of_birth', 'profile_picture'
        )

    def update(self, instance, validated_data):
        """Update user instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance