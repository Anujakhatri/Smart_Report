import logging
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import validate_password

from .serializers import RegistrationSerializer, SmartReportLoginSerializer, UserProfileSerializer

def register_page(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login.html")

def profile_page(request):
    return render(request, "profile.html")

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/profile/ - Retrieve user profile details
    PUT /api/auth/profile/ - Update user profile details
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

logger = logging.getLogger(__name__)
# Create your views here.
class RegisterView(generics.CreateAPIView):
    """
      POST /api/auth/register/
      Open to everyone — creates citizen by default

      """
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        #auto login after registration - return tokens immediately
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "success",
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "tokens":{
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    """
       POST /api/auth/login/
       Returns access + refresh token + role

       """
    serializer_class = SmartReportLoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

class LogoutView(generics.GenericAPIView):
    """
      POST /api/auth/logout/
      Blacklists the refresh token — kills the session
      """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({
                    "error":"Refresh token is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "logout success",
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            # invalid or expired tokens
            logger.warning(f"Token Error: {str(e)}")
            return Response({
                "error":"Invalid or expired token"
            }, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            #logout unexpected for debugging
            logger.error(f"Unexpected error during logout: {str(e)}", exc_info=True)
            return Response({
                "error":"Invalid or error occured"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)