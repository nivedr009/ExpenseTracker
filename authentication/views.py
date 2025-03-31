from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages  # Import messages framework
from expenses.models import Expense
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime

# Database connection settings
DB_CONFIG = {
    "dbname": "expense_db",
    "user": "expense_admin",
    "password": "expensepass",
    "host": "expense-container",  # Use Docker container name
    "port": "5432",  # Default PostgreSQL port
}

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check if email already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # Create user and log them in
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Automatically logs in the user

        #  Store success message in session (only shown once)
        request.session["registration_success"] = True  

        
        login(request, user)  # Automatically log in the user after registration
        return redirect("dashboard")  # Redirect to dashboar

    return render(request, "authentication/register.html")


def login_view(request):
    print("Login View Called")  # Debugging

    if request.method == 'POST':
        print("POST Request Received")  # Debugging
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")  # Debugging

        user = authenticate(request, username=username, password=password)  

        if user is not None:
            print("User authenticated successfully")  # Debugging
            login(request, user)
            return redirect('dashboard')  # Change 'dashboard' to the correct route
        else:
            print("Authentication failed")  # Debugging
            messages.error(request, "Invalid username or password.")  # Display error

    return render(request, "authentication/login.html")

@login_required
def dashboard(request):

     # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get the current date
    today = now()

    ## Filter the total income for the current month and for the logged-in user
    total_income = Expense.objects.filter(
        user=request.user,  # Filter by the current user
        transaction_type='Credit',
        date__month=current_month,
        date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0  # Default to 0 if no data is found

    # Calculate total expenses (Debit transactions) for the current month and for the logged-in user
    total_expenses = Expense.objects.filter(
        user=request.user,  # Filter by the current user
        transaction_type='Debit',
        date__year=today.year,  # Filter by the current year
        date__month=today.month  # Filter by the current month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Fetch the 5 most recent transactions for the logged-in user
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]

    # Calculate cumulative income (Credit transactions) for all time and for the logged-in user
    total_income_all_time = Expense.objects.filter(
        user=request.user,  # Filter by the current user
        transaction_type='Credit'
    ).aggregate(Sum('amount'))['amount__sum'] or 0  # Default to 0 if no data is found

    # Calculate cumulative expenses (Debit transactions) for all time and for the logged-in user
    total_expenses_all_time = Expense.objects.filter(
        user=request.user,  # Filter by the current user
        transaction_type='Debit'
    ).aggregate(Sum('amount'))['amount__sum'] or 0  # Default to 0 if no data is found

    # Calculate cumulative balance (total income - total expenses for all time)
    cumulative_balance = total_income_all_time - total_expenses_all_time

    return render(request, 'authentication/dashboard.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'recent_expenses': recent_expenses,
        'cumulative_balance': cumulative_balance,
    })

def logout_view(request):
    logout(request)
    return redirect('login')