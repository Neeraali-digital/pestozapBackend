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
            'is_verified', 'is_staff', 'is_superuser', 'full_name', 'profile', 'date_joined'
        )
        read_only_fields = ('id', 'is_verified', 'is_staff', 'is_superuser', 'date_joined')


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


class AdminCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating admin users.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        """Create admin user with staff and superuser privileges."""
        password = validated_data.pop('password')
        email = validated_data['email']
        
        # Generate username from email
        username = email.split('@')[0]
        
        user = User.objects.create_user(
            username=username,
            **validated_data,
            is_staff=True,
            is_superuser=True,
            is_verified=True
        )
        user.set_password(password)
        user.save()
        return user