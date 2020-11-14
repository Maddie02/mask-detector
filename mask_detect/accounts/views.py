from django.shortcuts import render


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    return render(request, 'accounts/register.html')