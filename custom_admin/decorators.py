from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def admin_panel_required(view_func):
    """
    Decorator for views that checks if the user is logged in and is either staff or a superuser.
    Redirects unauthenticated or unauthorized users to the admin login page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in with your administrative account to access the Admin Panel.')
            return redirect(f"{reverse('custom_admin:login')}?next={request.path}")
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Access denied. You do not have administrator privileges.')
            return redirect('custom_admin:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
