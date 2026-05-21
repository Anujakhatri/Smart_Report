# Django REST Framework (DRF) JWT Authentication & Authorization Guide

This guide provides a comprehensive, step-by-step roadmap to start any new backend project with custom authentication and authorization from scratch. It is based on the robust **Django + DRF + Django REST Framework SimpleJWT** pattern used in your current project.

---

## 🏗️ Phase 1: Environment Setup

Always start by creating a clean virtual environment and installing the required packages.

### 1. Initialize Virtual Environment & Install Dependencies
Run these commands in your terminal:

```bash
# Create a virtual environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Install required packages
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

### 2. Create Django Project and App
```bash
# Create the main project
django-admin startproject my_project .

# Create the authentication/user management apps
python manage.py startapp accounts
```

---

## ⚙️ Phase 2: Configuration (`settings.py`)

Open `my_project/settings.py` and modify the following configurations:

### 1. Register Apps & Middleware
Add your auth app, REST framework, and CORS headers package:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-Party Apps
    'rest_framework',
    'corsheaders',
    
    # Custom Apps
    'accounts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Put this at the very top!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Needed for request.user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 2. Configure DRF & SimpleJWT
Add this configuration block to enforce JWT authentication globally while allowing flexible permissions:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Protect all endpoints by default
    ),
}

# Optional: Customize JWT lifetimes
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 3. Point Django to your Custom User Model
Under the `INSTALLED_APPS` or at the bottom, declare:
```python
AUTH_USER_MODEL = 'accounts.User'
```

### 4. Setup CORS Rules
Allow frontend origins (e.g. React running on port 5173):
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# Or during local development only:
# CORS_ORIGIN_ALLOW_ALL = True 
```

---

## 👤 Phase 3: The Custom User Model (`accounts/models.py`)

> [!IMPORTANT]
> **Django Golden Rule:** Always configure a custom User model at the start of your project *before* running your first migrations. Changing the User model mid-project is highly complex.

Create a robust custom User model that supports roles and handles password hashing automatically when updated:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='patient'
    )

    @property
    def effective_role(self):
        if self.is_superuser:
            return 'admin'
        return self.role

    def save(self, *args, **kwargs):
        # Automatically hash password if it has not been hashed yet
        if self.password and not (
            self.password.startswith('pbkdf2_sha256$') or 
            self.password.startswith('bcrypt$') or 
            self.password.startswith('argon2$')
        ):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
```

---

## 📝 Phase 4: Serializers & Registration (`accounts/serializers.py`)

Create a serializer that handles user creation and ensures passwords remain write-only (hidden from frontend payloads):

```python
from rest_framework import serializers
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True}  # Protects password from showing in response
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'patient')
        )
        return user
```

---

## ⚡ Phase 5: Views and Endpoints (`accounts/views.py`)

Set up views for user registration and profile details with proper authentication constraints:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # NOTE: If you have sub-profiles (like Doctor/Patient profiles),
        # create them here by checking: if user.role == 'doctor': ...
        
        return Response({"message": "Registration successful"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    
    if request.method == 'GET':
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.effective_role,
        })

    elif request.method == 'PUT':
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.save()
        return Response({"message": "Profile updated successfully"})
```

---

## 🔗 Phase 6: URL Routing

### 1. Account App Routes (`accounts/urls.py`)
```python
from django.urls import path
from .views import register, profile

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]
```

### 2. Main Project Routes (`my_project/urls.py`)
Wire up the app endpoints alongside standard SimpleJWT endpoints for logging in (obtaining tokens) and renewing sessions (refreshing tokens):

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Token Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Custom Account Endpoints
    path('api/accounts/', include('accounts.urls')),
]
```

---

## 🚀 Phase 7: Run Migrations and Start Coding

Execute database updates to create the custom user table:

```bash
# 1. Create migration files
python manage.py makemigrations accounts

# 2. Run migrations
python manage.py migrate

# 3. Create a superuser
python manage.py createsuperuser

# 4. Start the server!
python manage.py runserver
```

You now have a fully functional, high-performance JWT token-based authentication and custom authorization (role-based) backend server ready to power your next application! 🚀
