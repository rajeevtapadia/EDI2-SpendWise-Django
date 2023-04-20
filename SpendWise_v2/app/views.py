from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "index.html", {})

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('usrnm')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        email = request.POST.get('email')

        if pass1 != pass2:
            return HttpResponse("Passwords don't match please try again")
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
            return HttpResponse('username or password is incorrect')
    return render(request, 'login.html', {})

def home_pg(request, *args, **kwargs):
    return render(request, "home.html", {})

# def Logout(request):
#     return render(request, )
