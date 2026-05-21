from urllib.robotparser import normalize

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


# controls what data comes in (request)
# controls what data goes out (response)
# validates everything before touching the database
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')
        extra_kwargs = {
            'role': {'default': 'citizen'},
        }

    def validate_username(self, value):
        value = value.strip()
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError(
                "Username may only contain letters, numbers, and underscores."
            )
        return value
    def validate_email(self, value):
        normalized = value.strip().lower()
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("This email is already registered.")
        return normalized

    def validate_role(self,value):
        ALLOWED_SELF_ROLES = ['citizen']  # only citizen can self-register
        if value not in ALLOWED_SELF_ROLES:
            raise serializers.ValidationError(
                "You cannot self-register with this role."
            )
        return value
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'citizen')
        )


# ─────────────────────────────────────────────────────
# 2. LOGIN SERIALIZER
#    Purpose  → verify credentials + return JWT tokens
#    Used by  → LoginView
#    Methods  → POST only
#    NOTE     → does NOT touch DB, no model needed
# ─────────────────────────────────────────────────────
class SmartReportLoginSerializer(TokenObtainPairSerializer):
    """
    Extends SimpleJWT's default login to also return
    role + username so the frontend knows where to redirect.

    Default TokenObtainPairSerializer already handles:
       checking username/password
       raising 401 if wrong credentials
       generating access + refresh tokens

    We just ADD extra fields to the response.
    """
    def validate(self, attrs):
        # let simplejwt do all the credential checking
        data=super().validate(attrs)

        # attach extra info to the token response
        data['role'] =self.user.role
        data['username']=self.user.username
        data['email']=self.user.email
        data['user_id']=self.user.id
        return data