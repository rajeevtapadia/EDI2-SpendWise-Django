from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime

from .forms import ExpenseForm
from .models import Expense

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
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('/profile/' + username)
        else:
            messages.info(request, 'Wrong Username or Password')
            return redirect('login')

    return render(request, 'login.html', {})


@login_required(login_url='login')
def home_pg(request, *args, **kwargs):
    return render(request, "home.html", {})


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request, pk):
    # print(request.method)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        # print(form.description)
        if form.is_valid():
            print(form.cleaned_data['description'])
            newExpense = Expense(profile=pk)
            # newExpense.profile = pk
            newExpense.description = form.cleaned_data['description']
            newExpense.amount = form.cleaned_data['amount']
            # newExpense.date = form.cleaned_data['date']
            newExpense.payment_mode = form.cleaned_data['mode']
            newExpense.category = form.cleaned_data['category']
            newExpense.save()
            print('expence added successfully')
    else:
        form = ExpenseForm()



    return render(request, 'dashboard.html', {'usr': pk, 'form':form})

