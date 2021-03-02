from django.contrib import admin
from .models import Statistic, Violation

admin.site.register(Statistic)
admin.site.register(Violation)