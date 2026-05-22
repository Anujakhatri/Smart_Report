from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

# controls what data comes in (request)
# controls what data goes out (response)
# validates everything before touching the database

User = get_user_model()

# ─────────────────────────────────────────────────────
#1.Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    """
    Validates fields and creates the user.
    Token minting is the view's job — not here.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'phone_number', 'province')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:               # ✅ was missing entirely
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data['password2'] = validated_data['password']
        return User.objects.create(**validated_data)


# ─────────────────────────────────────────────────────
# 2. LOGIN SERIALIZER

class LoginSerializer(TokenObtainPairSerializer):
    """
        get_token()  → embeds claims inside the JWT payload itself
        validate()   → attaches user info to the HTTP response body
                       frontend reads roles here and redirects — no extra call needed
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['roles'] = [r.codename for r in user.get_roles()]
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id':          self.user.id,
            'username':    self.user.username,
            'email':       self.user.email,
            'roles':       [r.codename for r in self.user.get_roles()],   #  not self.user.roles
            'permissions': [p.codename for p in self.user.get_permissions()],
        }
        return data



class LogoutSerializer(serializers.Serializer):
    """
    validate() → confirms token string is present
    save()     → blacklists it so /token/refresh/ returns 401
    Business logic lives here, not in the view.
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token_string = attrs['refresh']
        return attrs

    def save(self):
        try:
            RefreshToken(self.token_string).blacklist()
        except TokenError:
            raise serializers.ValidationError('Token is invalid or already blacklisted.')

class UserProfileSerializer(serializers.ModelSerializer):
    """
     roles → SerializerMethodField because it's get_roles() not a db column.
     Used only on settings page: view info or edit phone/province.
     """
    roles = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'roles', 'phone_number', 'province')
        read_only_fields = ('id', 'roles')

    def get_roles(self, obj):
        return [r.codename for r in obj.get_roles()]