from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm


def logout_request(request):
    logout(request)
    messages.info(request,"You are logged out")
    return redirect("main:homepage")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("main:user")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username = username,password = password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are logged as {username}")
                    return redirect("main:homepage")
                else:
                    messages.error(request,"Username or password don't match")
            else:
                messages.error(request,"Username or password don't match")
        form = AuthenticationForm()
        return render(request,
                    "main/login.html",
                    {"form":form})