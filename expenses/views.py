from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .models import Expense
from django.contrib import messages

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Link the expense to the logged-in user
            expense.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')  # Fetch expenses for the logged-in user
    return render(request, 'expenses/list_expenses.html', {'expenses': expenses})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  # Ensure the expense belongs to the logged-in user

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)  # Bind the form to the existing expense
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('list_expenses')  # Redirect to the expenses list page
    else:
        form = ExpenseForm(instance=expense)  # Pre-fill the form with the existing expense data

    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  # Ensure the expense belongs to the logged-in user

    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect('list_expenses')  # Redirect to the expenses list page

    return render(request, 'expenses/delete_expense.html', {'expense': expense})