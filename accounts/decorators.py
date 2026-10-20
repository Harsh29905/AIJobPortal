from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def candidate_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if not (request.user.is_candidate or request.user.is_superuser):
            messages.error(request, "Access restricted. This page is only for Job Seekers.")
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def recruiter_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if not (request.user.is_recruiter or request.user.is_superuser):
            messages.error(request, "Access restricted. This page is only for Recruiters.")
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
