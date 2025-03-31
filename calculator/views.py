from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from datetime import datetime

# Registration view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Create the user if all validations pass
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)  # Log in the user automatically
            return redirect('home')  # Redirect to a page after registration (e.g., home page)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    months = MonthWise.objects.all()  # Get all months from the database
    expenses = Expense.objects.filter(month_wise__user_id = request.user.id).order_by('-date')
    print(expenses)
    return render(request, 'home.html', {'months': months,'expenses':expenses})

# View for adding a new month and salary
def add_month(request):
    if request.method == 'POST':
        new_month = request.POST.get('new_month')
        monthly_salary = request.POST.get('monthly_salary')
        working_hour = request.POST.get('working_hour')

        print(monthly_salary,'monthly_salary')

        # Split the 'YYYY-MM' value into year and month
        year, month = new_month.split('-')  # 'YYYY' and 'MM'
        daily_salary = int(monthly_salary) / 30

        minute_salary = daily_salary / (int(working_hour) * 60)

        # Calculate the first day of the month (1st day of the selected month)
        first_day_of_month = datetime(int(year), int(month), 1)
        # Create a new Month entry
        month = MonthWise(month=first_day_of_month, salary=monthly_salary,working_hours_per_day=working_hour,user_id=request.user.id,per_day_salary=daily_salary,per_minute_salary=minute_salary)
        month.save()

        messages.success(request, f"New month {new_month} added successfully!")
        return redirect('home')

    return redirect('home')

# View for the main expense form
def expense_form(request):

    if request.method == 'POST':
        # Handle expense form submission
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        month = datetime.strptime(date, '%Y-%m-%d').replace(day=1)
        try:
            month_obj = MonthWise.objects.get(month=month,user_id=request.user.id)
        except MonthWise.DoesNotExist:
            messages.error(request, "Add income for the month first")
        except Exception as e:
            print(e)
            messages.error(request, "Add income for the month first")
            return redirect('home')
        print(description,amount,month)
        # Save the expense to the database
        expense = Expense(description=description, amount=amount, month_wise=month_obj,date=date)
        expense.save()

        messages.success(request, f"Expense for {description} added successfully!")
        return redirect('home')

    return redirect('home')

