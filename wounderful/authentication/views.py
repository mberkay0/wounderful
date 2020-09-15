from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserUpdateForm

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("images")
            else:    
                messages.warning(request, 'You entered an incorrect username or password')
        else:
            messages.warning(request, 'Please enter username and password')

    return render(request, "accounts/login.html", {"form": form})


def register_user(request):

    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('/')       

    return render(request, "accounts/register.html", {"form": form})


@login_required(login_url='/user/login')
def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/user/login')
def user_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully changed!')
            return redirect('user_menu')
        else:
            messages.error(request, 'Please fill in the fields correctly')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form':form
    }

    return render(request, 'accounts/change_password.html', context)


@login_required(login_url='/user/login')
def user_menu(request):

    return render(request, 'accounts/user.html')


@login_required(login_url='/user/login')
def user_update(request):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('user_menu')
        else:
            messages.error(request, 'Please fill in the fields correctly')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form':form
    }

    return render(request, 'accounts/user_update.html', context)
