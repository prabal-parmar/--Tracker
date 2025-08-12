from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from tracker.models import Expense
import uuid
from datetime import datetime
# Create your views here.

# Home Page
def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    
    if request.method=="POST":
        amount=request.POST.get('amount')
        reason=request.POST.get('reason')
        date=request.POST.get('date') or datetime.now()
        try:
            newtracker=Expense(user=request.user, expense=amount, reason=reason, date=date, expense_id=uuid.uuid4())
            newtracker.save()
        except:
            # prompt to be added
            pass
    
    # allexpenses = Expense.objects.filter(user=request.user).values()
    presentMonth, totalExpenses = claculateThisMonthExpense(request.user)
    content = {
        'user': request.user,
        'data': reversed(presentMonth),
        'total': totalExpenses
    }
    return render(request, 'index.html', content)

# Login
def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html')
        
    return render(request, 'login.html')

#Logout
def logoutUser(request):
    logout(request)
    return redirect('login')

#Register
def register(request):
    if request.method=="POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
            user.save()
            userlogin = authenticate(username=username, password=password)
            login(request, userlogin)
            return redirect('/')
        except:
            # prompt to be added
            return redirect('/register')
        
    return render(request, 'register.html')

#Profile Section
def profile(request):
    if request.user.is_anonymous:
        return redirect('/login')
    
    expenses=Expense.objects.filter(user=request.user).values()
    totalExpenses = 0
    for exp in expenses:
        totalExpenses += exp['expense']
    
    content = {
        'user': request.user,
        'total_expenses': totalExpenses
    }
    return render(request, 'profile.html', content)

#About Tracker
def about(request):
    return render(request, 'about.html')

#Delete Expenses
def deleteExpense(request, id):
    expenseCard=Expense.objects.get(expense_id=id)
    expenseCard.delete()
    return redirect('/')

#Update Expenses
def updateExpense(request, id):
    expense_data = Expense.objects.get(expense_id=id)
    if request.method=="POST":
        amount=request.POST.get('amount')
        reason=request.POST.get('reason')
        date=request.POST.get('date') or expense_data.date
        expense_data.expense=amount
        expense_data.reason=reason
        expense_data.date=date
        expense_data.save()
        return redirect('/')
    
    content = {
        'expense': expense_data.expense,
        'reason': expense_data.reason,
        'date': expense_data.date
    }

    return render(request, 'update_expense.html', content)

#Update Profile
def updateProfile(request):
    if request.method=="POST":
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get("email")
        username=request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            user.first_name=firstname
            user.last_name=lastname
            user.email = email
            user.username=username
            user.save()
        except:
            #prompt
            pass
        return redirect('profile')
    
    expenses=Expense.objects.filter(user=request.user).values()
    totalExpenses = 0
    for exp in expenses:
        totalExpenses += exp['expense']
    
    content = {
        'total_expenses': totalExpenses
    }
    return render(request, 'update_profile.html', content)

#All Expenses
def allExpenses(request):
    expenses=Expense.objects.filter(user=request.user).values()
    totalExpenses = 0
    for exp in expenses:
        totalExpenses += exp['expense']
    content = {
        'data': expenses,
        'total_expenses': totalExpenses
    }
    return render(request, 'overall_expenses.html', content)


# Function to filter out this month expenses
def claculateThisMonthExpense(user):
    allExpenses=Expense.objects.filter(user=user).values()
    month=datetime.now().month
    year=datetime.now().year
    thisMonthExpenses=[]
    total = 0
    for expense in allExpenses:
        if expense['date'].month == month and expense['date'].year == year:
            thisMonthExpenses.append(expense)
            total += expense['expense']
        # print(expense['date'].month)
    return thisMonthExpenses, total