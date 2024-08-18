from django import forms
from .models import ProductEnter

class ProductEnterForm(forms.ModelForm):
    class Meta:
        model = ProductEnter
        fields = ['product', 'quantity', 'old_quantity', 'date', 'description']
