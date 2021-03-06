from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .forms import SignUpEmployeeForm, UpdateEmployeeProfilePicture
from .models import Employee
from stats.models import Statistic, Violation
from stats.views import get_detailed_chart_for_employee
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
    
    if request.method == 'POST':
        profile_form = UpdateEmployeeProfilePicture(request.POST, request.FILES, instance=request.user)
    
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'You have updated your profile picture!')
            return redirect('profile')
    else:
        profile_form = UpdateEmployeeProfilePicture(instance=request.user)


    user_stats = Statistic.objects.filter(employee=request.user).first()
    
    if user_stats == None:
        context = {
            'p_form': profile_form
        }
    else:
        context = {
            'last_seen_without_mask': user_stats.last_seen_without_mask,
            'p_form': profile_form
        }

    return render(request, 'accounts/profile.html', context)


@staff_member_required
def employee_profile(request):
    employee_id = request.GET['employee_id']
    employee = Employee.objects.filter(id=employee_id).first()

    violations = Violation.objects.filter(statistic__employee=employee)

    context = {
        'employee': employee,
        'violations': violations,
        'stat': Statistic.objects.filter(employee=employee).first(),
        'chart': get_detailed_chart_for_employee(violations)
    }
    
    return render(request, 'accounts/employee-profile.html', context)

