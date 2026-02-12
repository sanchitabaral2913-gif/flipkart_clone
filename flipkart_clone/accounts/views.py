from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ✅ Sabse pehle welcome page
            return redirect('welcome')

        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def welcome_view(request):
    return render(request, 'accounts/welcome.html')