from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm


def signup_view(request):
    """Register a new user and log them in on success."""
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome to Watch House!')
            return redirect('products:home')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Authenticate an existing user."""
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Honour ?next= so login redirects work for protected pages
            next_url = request.GET.get('next')
            return redirect(next_url or 'products:home')
        messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log the current user out."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('products:home')
