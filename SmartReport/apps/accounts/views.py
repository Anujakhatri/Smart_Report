import logging
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UserProfileSerializer

logger = logging.getLogger(__name__)

def register_page(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login.html")

def profile_page(request):
    return render(request, "profile.html")


# Create your views here.
class RegistrationView(APIView):
    """
      POST /api/auth/register/
      Open to everyone — serializer creates citizen(user) by default and view mint the tokens.

      """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        #auto login after registration - return tokens immediately
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Registration success",
            "user":{
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "roles": [r.codename for r in user.get_roles()],  # <--not user.role
            },
            "tokens":{
                "refresh": str(refresh),
                "access": str(refresh.access_token),
             }
        }, status=status.HTTP_201_CREATED)

#================= Login =================================
class LoginView(TokenObtainPairView):
    """
       POST /api/auth/login/
       Returns access + refresh token + roles --> frontend redirects based on role
       No profile call needed after this view
       """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

#================= Logout =================================
class LogoutView(generics.GenericAPIView):
    """
      POST /api/auth/logout/
      Blacklists the refresh token — kills the session
      """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logout success"}, status=status.HTTP_200_OK)

#================= Profile =================================
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/profile/ - Retrieve user profile details
    PUT /api/auth/profile/ - Update user profile details
    NOT used for role-based redirect - login response handles first
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
