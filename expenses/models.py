from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Other', 'Other'),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('Credit', 'Credit'),  # Income
        ('Debit', 'Debit'),    # Expense
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')  # Link expense to a user  # Link expense to a user
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Expense amount
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='Debit')  # New field
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Expense category
    description = models.TextField(blank=True, null=True)  # Optional description
    date = models.DateField()  # Date of the expense
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"{self.category} - {self.amount}"