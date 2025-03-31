from django import forms
from .models import Expense
from datetime import date  
from django.utils.timezone import now

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['transaction_type', 'amount', 'category', 'description', 'date']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter a description'}),
            'date': forms.DateInput(attrs={'type': 'date', 'value': date.today()}),  # Set default date to today
        }
    
    def clean_date(self):
        """Ensure that the date field always stores the current time as well."""
        selected_date = self.cleaned_data['date']
        current_time = now()
        return current_time.replace(year=selected_date.year, month=selected_date.month, day=selected_date.day, hour=current_time.hour, minute=current_time.minute, second=current_time.second)
    
     # Add an empty default option for category selection
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [("", "Select Category...")] + list(Expense.CATEGORY_CHOICES)
        
     # Use the CATEGORY_CHOICES from the Expense model
    category = forms.ChoiceField(
        choices=Expense.CATEGORY_CHOICES,  # Use the predefined choices
        widget=forms.Select(attrs={'class': 'form-control category-dropdown'}),  # Add custom class
    )
