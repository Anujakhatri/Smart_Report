from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'phone_number', 'province')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

from SmartReport.constants import ROLE_PORTAL_MAP

class LoginSerializer(TokenObtainPairSerializer):
    """Custom token serializer that embeds roles and permissions."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        
        roles = [r.codename for r in user.get_roles()]
        token['roles'] = roles
        token['permissions'] = [p.codename for p in user.get_permissions()]
        
        # Add portal claim
        portal = None
        for role in roles:
            if role in ROLE_PORTAL_MAP:
                portal = ROLE_PORTAL_MAP[role]
                break
        if portal:
            token['portal'] = portal
            
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        roles = [r.codename for r in self.user.get_roles()]
        permissions = [p.codename for p in self.user.get_permissions()]
        
        portal = None
        for role in roles:
            if role in ROLE_PORTAL_MAP:
                portal = ROLE_PORTAL_MAP[role]
                break
                
        data['roles'] = roles
        data['permissions'] = permissions
        data['portal'] = portal
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'roles': roles,
            'permissions': permissions,
            'portal': portal,
        }
        return data


class LogoutSerializer(serializers.Serializer):
    """Serializer to handle logout by blacklisting the refresh token."""
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token_string = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token_string).blacklist()
        except TokenError:
            raise serializers.ValidationError('Token is invalid or already blacklisted.')


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating user profile with assigned roles."""
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'roles', 'phone_number', 'province')
        read_only_fields = ('id', 'roles')

    def get_roles(self, obj):
        return [r.codename for r in obj.get_roles()]