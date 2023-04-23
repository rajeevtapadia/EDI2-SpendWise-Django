from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


# Create your views here.

# put login requried decorator before the view you want to restrict
def home_view(request, *args, **kwargs):
    return render(request, "index.html", {})

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('usrnm')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        email = request.POST.get('email')

        if pass1 != pass2:
            messages.info(request, "Password Not Matching")
            return redirect('signup')
            # return HttpResponse("Passwords don't match please try again")
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('signup')
        else:
            myUser = User.objects.create_user(username, email, pass1)
            myUser.save()
            return HttpResponseRedirect('/login')
    return render(request, 'signup.html', {})

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('usrnm')
        pass1 = request.POST.get('pass')

        user = authenticate(request, username = username, password = pass1)
        if user is not None:
            login(request, user)
            return redirect('/home2')
        else:
            messages.info(request, 'Wrong Username or Password')
            return redirect('login')
            # return HttpResponse('username or password is incorrect')
    return render(request, 'login.html', {})

@login_required(login_url='login')
def home_pg(request, *args, **kwargs):
    return render(request, "home.html", {})

@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('home')

def profile(request, pk):
    return render(request, )