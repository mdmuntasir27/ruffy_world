from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    RegisterForm, ProfileUpdateForm,
    ForgotPasswordLookupForm, DirectResetPasswordForm
)
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Ruffy World, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    from adoptions.models import AdoptionRequest
    from pets.models import Favorite
    from community.models import AdoptionPost, AdoptionInquiry

    # Ensure profile exists
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    recent_requests = AdoptionRequest.objects.filter(user=request.user).select_related('pet')[:5]
    favorite_pets = Favorite.objects.filter(user=request.user).select_related('pet')
    my_posts = AdoptionPost.objects.filter(author=request.user)
    my_inquiries = AdoptionInquiry.objects.filter(requester=request.user).select_related('post')[:5]

    context = {
        'recent_requests': recent_requests,
        'favorite_pets': favorite_pets,
        'my_posts': my_posts,
        'my_inquiries': my_inquiries,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


def forgot_password_view(request):
    """
    Profile-verification password recovery:
    User inputs username or email. If found, user is redirected directly
    to the reset password form (no console email / SMTP tokens).
    """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = ForgotPasswordLookupForm(request.POST)
        if form.is_valid():
            user = form.matched_user
            request.session['reset_password_user_id'] = user.pk
            messages.success(request, f'Account verified for {user.username}! You can now set your new password.')
            return redirect('reset_password_direct')
    else:
        form = ForgotPasswordLookupForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_password_direct_view(request):
    """
    Allows user to set a new password after successful profile verification.
    Requires strong or very strong password criteria.
    """
    if request.user.is_authenticated:
        return redirect('home')
    user_id = request.session.get('reset_password_user_id')
    if not user_id:
        messages.error(request, 'Please verify your profile first to reset your password.')
        return redirect('forgot_password')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User account not found. Please try again.')
        return redirect('forgot_password')

    if request.method == 'POST':
        form = DirectResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            if 'reset_password_user_id' in request.session:
                del request.session['reset_password_user_id']
            messages.success(request, 'Your password has been successfully reset! You can now log in.')
            return redirect('login')
    else:
        form = DirectResetPasswordForm()

    return render(request, 'accounts/reset_password_direct.html', {
        'form': form,
        'reset_username': user.username
    })
