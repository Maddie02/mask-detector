from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

class SignUpEmployeeForm(UserCreationForm):

    email = forms.EmailField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))

    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)

