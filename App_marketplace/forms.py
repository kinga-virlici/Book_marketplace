from django import forms

from book_review.models.book_review import BookReview
from .models.product import Product
from .models.order import OrderItem
from .models.mesage import Mesaj
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# in acest fisier cream formulare personalizate
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'author', 'description', 'price', 'image', 'quantity', 'book_available']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['class'] = 'form-control'


class MesajForm(forms.ModelForm):
    class Meta:
        model = Mesaj
        fields = ['name', 'email', 'phone', 'message']


class RegisterForm(UserCreationForm): # aici am definit o clasa cu ajutorul caruia putem gestiona formularul pt register
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'row gy-4'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'row gy-4'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'row gy-4'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'row gy-4'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['reviewer_name', 'book_title', 'image', 'review_content']
