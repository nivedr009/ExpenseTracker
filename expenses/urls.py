from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),  # URL for adding expenses
    path('list/', views.list_expenses, name='list_expenses'),  # List Expenses Page
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),  # Edit Expense Page
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),  # Delete Expense Page
    path('', views.list_expenses, name='list_expenses'),
    
]