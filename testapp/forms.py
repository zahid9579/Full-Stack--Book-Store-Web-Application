from django import forms
from .models import Book, DeliveryInfo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['user', 'author', 'photo', 'title', 'price', 'description']  # Include 'author'

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        

# for the delivery address imformation

class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo  
        fields = ['name', 'email', 'address1', 'address2', 'city', 'state', 'pincode', 'phone_number']