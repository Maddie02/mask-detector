from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

class SignUpEmployeeForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'company',)

