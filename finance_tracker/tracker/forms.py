from django import forms
from .models import Transaction,Category
from django.shortcuts import get_list_or_404


class TransactionForm(forms.Form):
    transaction_name=forms.CharField(max_length=100)
    amount=forms.DecimalField(decimal_places=0)
    transaction_Type=forms.ChoiceField(choices=[("income","Income"),("expense","Expense")])
    category=forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class': 'form-select'}))
    date=forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'] 
    )

    pass