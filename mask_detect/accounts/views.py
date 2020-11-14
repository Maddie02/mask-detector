from django.shortcuts import render, redirect
from .forms import SignUpEmployeeForm
from django.contrib import messages

def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = SignUpEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Welcome, {first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = SignUpEmployeeForm()
    return render(request, 'accounts/register.html', {'form': form})

