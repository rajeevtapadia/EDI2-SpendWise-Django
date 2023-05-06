# add your forms

from django import forms
from datetime import datetime
from . models import Expense
from django.db import models


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
    

class ExpenseFormV2(forms.ModelForm):
    class Meta:
        # profile = models.ForeignKey(User, on_delete=models.CASCADE)
        model = Expense
        fields = ['description', 'amount', 'date', 'payment_mode', 'category']
        lables = {'description':'description', 
                  'amount':'amt', 'date':'date', 'payment_mode':'mode', 'category':'cat'}
    def __init__(self, *args, **kwargs):
        super(ExpenseFormV2, self).__init__(*args, **kwargs)
        
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['amount'].widget.attrs['placeholder'] = 'Amount'
        self.fields['date'].widget.attrs['placeholder'] = 'Date'
        self.fields['payment_mode'].widget.attrs['placeholder'] = 'Mode of Payment'