from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from .forms import RegisterUserForm

def login_user(request):
    copy_time = datetime.now().year
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Error in login...")
                return redirect("login-user")
        else:
            return render(request, "authenticate/login.html", {
                "copy_time" : copy_time,
            })
    else:
        messages.error(request, "Already logged in...")
        return redirect("home")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Logged out...")
        return redirect("home")
    else:
        messages.error(request, "Not logged in...")
        return redirect("home")

def register_user(request):
    copy_time = datetime.now().year
    if not request.user.is_authenticated:
        if request.method == "POST":
            form= RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "Account Created...")
                return redirect("home")
        else:
            form= RegisterUserForm()
        return render(request, "authenticate/register_user.html", {
            "copy_time" : copy_time,
            "form" : form,
        })
    else:
        messages.error(request, "Already logged in...")
        return redirect("home")
