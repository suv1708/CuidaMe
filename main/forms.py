# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Medico, Paciente


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password'}))


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especializacion']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = []
