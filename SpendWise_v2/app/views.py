from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime

from .forms import ExpenseForm, ExpenseFormV2
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
    # code handeling the form submission
    if request.method == "POST":
        form = ExpenseFormV2(request.POST)
        form.instance.profile = request.user
        # updating the balence
        bal = request.user.profile.balence
        if form.is_valid():
            form.save()
            request.user.profile.balence = bal - int(request.POST.get('amount'))
            request.user.profile.save()
            # redirecting or else the resubmission problem occurs
            return redirect('/profile/' + request.user.username)
    else:
        # code to just display form
        form = ExpenseFormV2()

    # enumarating total expense
    totalAmountSpent = Expense.sum(Expense, 'all', request.user)

    # enumarating number of expenses
    noOfExp = Expense.objects.count() - 3

    # enumarating categorywise sum
    categorySumList = []
    for value, name in Expense.CATEGORY_CHOICES:
        categorySumList.append(Expense.sum(Expense, value, request.user))

    # expense list for table
    expList = Expense.objects.filter(profile=request.user.id)

    # balence
    balence = request.user.profile.balence

    context = {'usr': request.user.username,
               'form':form, 
               'expList': expList.reverse(),
               'Expense': Expense,
               'categorySumList':categorySumList,
               'totalAmountSpent':totalAmountSpent,
               'noOfExp':noOfExp,
               'balence':balence,}
    
    return render(request, 'dashboard.html', context)


# edit expense view
def editExpView(request, pk, id):
    current_expense = Expense.objects.get(id=id)
    if request.method == "POST":
        bal = request.user.profile.balence
        old_amt = int(current_expense.amount)

        if 'delete' in request.POST:
            # Handle delete action
            # current_expense = Expense.objects.get(id=id)
            request.user.profile.balence = bal + int(current_expense.amount)
            current_expense.delete()
            request.user.profile.save()
            return redirect('/profile/' + request.user.username)
        else:
            # Handle edit action
            edit_form = ExpenseFormV2(request.POST)
            edit_form.instance.profile = request.user
            if edit_form.is_valid():
                # current_expense = Expense.objects.get(id=id)
                new_amt = int(request.POST.get('amount'))
                request.user.profile.balence = bal - new_amt + old_amt
                edit_form = ExpenseFormV2(request.POST, instance=current_expense)
                edit_form.save()
                request.user.profile.save()
                return redirect('/profile/' + request.user.username)
    else:
        # code just to display form with values form database
        # current_expense = Expense.objects.get(id=id)
        edit_form = ExpenseFormV2(instance=current_expense)
    return render(request, 'edit.html', {'edit_form': edit_form})

# set balence view
def setBal(request, pk):
    if request.method == 'POST':
        input_bal = request.POST.get('bal')
        if input_bal.isnumeric():
            request.user.profile.balence = int(input_bal)
            request.user.profile.save()
        return redirect('/profile/' + request.user.username)
    else:
        return render(request, 'set balence.html', {'usr': request.user.username,})