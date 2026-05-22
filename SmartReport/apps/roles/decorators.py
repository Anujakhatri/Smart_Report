from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from apps.roles.services import RBACService


def require_permission(permission_codename):
    """
    Decorator for function-based views.

    Usage:
        @api_view(['POST'])
        @require_permission('report.delete')
        def delete_report(request, pk):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication required.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            has_perm, reason = RBACService.has_permission(
                request.user,
                permission_codename
            )
            if not has_perm:
                return Response(
                    {'detail': f'Access denied. {reason}'},
                    status=status.HTTP_403_FORBIDDEN
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_admin():
    """Decorator requiring admin role."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_superuser:
                has_perm, _ = RBACService.has_permission(request.user, 'user.admin')
                if not has_perm:
                    return Response(
                        {'detail': 'Admin access required.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator