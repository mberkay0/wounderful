from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "placeholder":"Username"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", "placeholder":"Email"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "placeholder":"Password"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "placeholder":"Confirm Password"
            }
        ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'input', 'placeholder':'Username', 'help_text':'Opsiyonel'}),
            'email': forms.TextInput(attrs={'class':'input', 'placeholder':'Email', 'help_text':'Opsiyonel'}),
        }