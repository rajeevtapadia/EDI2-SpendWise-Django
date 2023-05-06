# add your forms

from django import forms
from datetime import datetime
from . models import Expense


class ExpenseForm(forms.Form):
    description = forms.CharField(label="desc", max_length=100, required=True)
    amount = forms.IntegerField(required=True, label='amt')
    # date has questionable behaviour
    # date = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'Keep Empty for now'}))
    mode = forms.CharField(label='payment mode', 
                           widget=forms.Select(choices=Expense.PAYMENT_MODE_CHOICES),
													 required=True)
    category = forms.CharField(label='category', 
                               widget=forms.Select(choices=Expense.CATEGORY_CHOICES),
															 required=True)
    