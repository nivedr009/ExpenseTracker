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
            messages.success(request, "Record added successfully!")
            return render(request, 'expenses/add_expense.html', {'form': ExpenseForm()})  # Render the same page with a new form
        else:
            messages.error(request, "There was an error in the form. Please correct it.")
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')  # Fetch expenses for the logged-in user
    return render(request, 'expenses/list_expenses.html', {'expenses': expenses})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        # Update the fields from the form
        expense.transaction_type = request.POST.get('transaction_type')
        expense.category = request.POST.get('category')
        expense.amount = request.POST.get('amount')
        expense.description = request.POST.get('description')
        expense.date = request.POST.get('date')  # Update the date field
        expense.save()  # Save the updated expense to the database
        
        # Add success message after saving
        messages.success(request, "Expense updated successfully!")  

        return redirect('list_expenses')  # Redirect to the list page after saving

    return render(request, 'expenses/edit_expense.html', {'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  # Ensure the expense belongs to the logged-in user

    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect('list_expenses')  # Redirect to the expenses list page

    return render(request, 'expenses/delete_expense.html', {'expense': expense})
