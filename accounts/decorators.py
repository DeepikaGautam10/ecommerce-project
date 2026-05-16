from functools import wraps

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect


def role_required(allowed_roles=None):
    """Restrict a view to staff / superuser accounts.

    ``allowed_roles`` is accepted purely for readable call sites
    (e.g. ``@role_required(['admin'])``); access is granted based on the
    user's ``is_staff`` / ``is_superuser`` flags.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to continue.')
                return redirect('accounts:login')

            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            raise PermissionDenied
        return wrapper
    return decorator
