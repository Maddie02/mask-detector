from django.contrib import admin
from .models import Company, Employee
from .forms import SignUpEmployeeForm
from django.contrib.auth.admin import UserAdmin

class EmployeeUserAdmin(UserAdmin):
    model = Employee
    add_form = SignUpEmployeeForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'company', 'profile_pic')
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'company', 'is_staff', )

admin.site.register(Company)
admin.site.register(Employee, EmployeeUserAdmin)