from django import forms
from account.models import UserProfile
from django.contrib.auth.models import User

class AttendanceForm(forms.Form):
    attend = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nama Lengkap', 'required': True}))
    initial = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Inisial', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password', 'required': True}))

# class LoginForm(forms.Form):
#     initial = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Inisial', 'required': True}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password', 'required': True}))