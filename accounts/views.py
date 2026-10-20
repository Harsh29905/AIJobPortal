from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CandidateRegistrationForm,
    RecruiterRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
)


def register_candidate(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}! Your Job Seeker profile has been created successfully.")
            return redirect('candidate_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CandidateRegistrationForm()
    return render(request, 'accounts/register_candidate.html', {'form': form})


def register_recruiter(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}! Your Recruiter profile for {user.recruiter_profile.company_name} is ready.")
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecruiterRegistrationForm()
    return render(request, 'accounts/register_recruiter.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('dashboard_redirect')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def dashboard_redirect(request):
    if request.user.is_candidate:
        return redirect('candidate_dashboard')
    elif request.user.is_recruiter:
        return redirect('recruiter_dashboard')
    elif request.user.is_staff or request.user.is_superuser:
        return redirect('/admin/')
    return redirect('home')


@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account settings updated successfully.")
            return redirect('profile_settings')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_settings.html', {'form': form})
