from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

class SignUpEmployeeForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'company',)

