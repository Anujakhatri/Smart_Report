from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from apps.core.constants import ROLE_PORTAL_MAP

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
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
        user = User.objects.create_user(**validated_data)

        from apps.roles.models import Role, UserRole
        try:
            citizen_role = Role.objects.get(codename='citizen')
            UserRole.objects.create(user=user, role=citizen_role)
        except Role.DoesNotExist:
            pass

        return user


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # DB hit: 2 queries — roles र permissions
        roles = [r.codename for r in user.get_roles()]
        permissions = [p.codename for p in user.get_permissions()]

        portal = None
        for role in roles:
            if role in ROLE_PORTAL_MAP:
                portal = ROLE_PORTAL_MAP[role]
                break

        token['username'] = user.username
        token['email'] = user.email
        token['roles'] = roles
        token['permissions'] = permissions
        token['portal'] = portal

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        access = AccessToken(data['access'])

        data['user'] = {
            'id': self.user.id,
            'username': access['username'],
            'email': access['email'],
            'roles': access['roles'],
            'permissions': access['permissions'],
            'portal': access.get('portal'),
        }
        return data


class LogoutSerializer(serializers.Serializer):
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
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'roles', 'phone_number', 'province')
        read_only_fields = ('id', 'roles')

    def get_roles(self, obj):
        return [r.codename for r in obj.get_roles()]