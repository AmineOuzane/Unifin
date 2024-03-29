from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'app-form-control', 'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'app-form-control', 'placeholder': 'Email'}))
    contact_no = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'app-form-control', 'placeholder': 'Contact No'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'app-form-control', 'placeholder': 'Message'}))

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']