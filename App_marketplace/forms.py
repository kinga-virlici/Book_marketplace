from django import forms
from .models.product import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'author', 'description', 'price', 'image', 'quantity', 'book_available']

