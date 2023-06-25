from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=150, label="Correo electronico", label_suffix="")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña", label_suffix="")

class RegisterForm(forms.Form):
    username = forms.EmailField(max_length=150, label="Correo electronico", label_suffix="")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña", label_suffix="")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Repetir Contraseña", label_suffix="")