# invoices/forms.py
from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['project', 'amount', 'due_date', 'status', 'notes']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }