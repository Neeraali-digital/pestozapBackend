"""
Views for the users app.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import UserProfile
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserProfileSerializer,
    AdminCreateSerializer
)

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the current user."""
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """
    View for updating user information.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the current user."""
        return self.request.user


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating extended user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Get or create user profile."""
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_profile_picture(request):
    """
    Upload profile picture for the authenticated user.
    """
    if 'profile_picture' not in request.FILES:
        return Response(
            {'error': 'No profile picture provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user
    user.profile_picture = request.FILES['profile_picture']
    user.save()

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_profile_picture(request):
    """
    Delete profile picture for the authenticated user.
    """
    user = request.user
    if user.profile_picture:
        user.profile_picture.delete()
        user.profile_picture = None
        user.save()

    return Response(
        {'message': 'Profile picture deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    Get user statistics.
    """
    user = request.user
    stats = {
        'total_users': User.objects.count(),
        'verified_users': User.objects.filter(is_verified=True).count(),
        'user_joined_date': user.date_joined,
        'profile_completion': calculate_profile_completion(user),
    }
    return Response(stats, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Create admin user with staff and superuser privileges",
    request_body=AdminCreateSerializer,
    responses={
        201: openapi.Response(
            description="Admin user created successfully",
            examples={
                "application/json": {
                    "message": "Admin user created successfully",
                    "user": {
                        "id": 1,
                        "email": "admin@example.com",
                        "first_name": "Admin",
                        "last_name": "User",
                        "is_staff": True,
                        "is_superuser": True
                    }
                }
            }
        ),
        400: "Bad Request - Invalid data"
    },
    tags=['Admin Management']
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_admin(request):
    """
    Create admin user - for initial setup only.
    """
    serializer = AdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Admin user created successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_profile_completion(user):
    """
    Calculate profile completion percentage.
    """
    fields = [
        user.first_name,
        user.last_name,
        user.email,
        user.phone_number,
        user.address,
        user.date_of_birth,
        user.profile_picture,
    ]
    
    completed_fields = sum(1 for field in fields if field)
    total_fields = len(fields)
    
    return round((completed_fields / total_fields) * 100, 2)