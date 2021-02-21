from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import SignUpEmployeeForm
from .models import Employee
from stats.models import Statistic
import datetime
import csv

def home(request):
    return render(request, 'accounts/home.html', {'home': 1})


def register(request):
    if request.method == 'POST':
        form = SignUpEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'{first_name}, your account has been created. You can now log in.')
            return redirect('login')
    else:
        form = SignUpEmployeeForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):

    user_stats = Statistic.objects.filter(employee=request.user).first()
    
    context = {
        'last_seen_without_mask': user_stats.last_seen_date
    }

    return render(request, 'accounts/profile.html', context)


