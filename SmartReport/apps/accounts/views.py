from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UserProfileSerializer

User = get_user_model()


class RegisterView(APIView):
    """View to handle user registration and automatically issue tokens on success."""
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Registration success",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "roles": [r.codename for r in user.get_roles()],
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class BasePortalLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            portal = response.data.get('user', {}).get('portal')  # ← user भित्र हेर्नु
            if portal != getattr(self, 'required_portal', None):
                return Response({"detail": "Access denied for this portal."}, status=403)
        return response

class CitizenLoginView(BasePortalLoginView):
    required_portal = 'citizen'

class WardLoginView(BasePortalLoginView):
    required_portal = 'ward'

class DistrictLoginView(BasePortalLoginView):
    required_portal = 'district'

class AdminLoginView(BasePortalLoginView):
    required_portal = 'admin'


class LogoutView(APIView):
    """View to handle logout by blacklisting the refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logout success"}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    """View to retrieve a user profile by pk."""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
