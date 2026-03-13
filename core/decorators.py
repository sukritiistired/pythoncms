from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def permission_required(permission, login_url='core:login'):
    """
    Checks if user is authenticated and has the specified permission.
    Redirects to login if not authenticated, or dashboard if no permission.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect(login_url)

            if not request.user.has_perm(permission):
                messages.error(request, "You do not have permission to access this page.")
                return redirect('core:dashboard')

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator