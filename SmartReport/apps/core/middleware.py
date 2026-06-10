from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.core.constants import ROLE_PORTAL_MAP

class PortalAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()
        
        self.PORTAL_URL_MAP = {
            '/citizen/':      ROLE_PORTAL_MAP['citizen'],
            '/ward/':         ROLE_PORTAL_MAP['ward_staff'],
            '/district/':     ROLE_PORTAL_MAP['district_admin'],
            '/admin/':        ROLE_PORTAL_MAP['national_admin'],
        }

    def __call__(self, request):
        path = request.path
        
        # Skip check for /login/ and /api/regions/
        if 'auth/login/' in path or path.startswith('/api/regions/') or path.startswith('/admin/'):
            return self.get_response(request)

        required_portal = None
        for prefix, portal_name in self.PORTAL_URL_MAP.items():
            if path.startswith(prefix):
                required_portal = portal_name
                break
                
        if required_portal:
            try:
                auth_tuple = self.jwt_authenticator.authenticate(request)
                if auth_tuple is not None:
                    user, token = auth_tuple
                    token_portal = token.get('portal')
                    
                    if token_portal != required_portal:
                        return JsonResponse({"detail": "Access denied for this portal."}, status=403)
            except Exception:
                pass # Let standard DRF auth handle missing/invalid token

        return self.get_response(request)
