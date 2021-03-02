"""mask_detect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from stats import views as stat_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name="home"),
    path('register/', accounts_views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('profile/', accounts_views.profile, name="profile"),
    path('profile/employee', accounts_views.employee_profile, name="employee-profile"),
    path('stats', stat_views.export_csv_stats, name='export-csv'),
    path('dashboard/', stat_views.dashboard, name="dashboard"),
    path('admin-stats/', stat_views.dashboard_export_csvs, name='export-all-stats'),
    path('delete-stats/', stat_views.delete_dashboard_stats, name="delete-stats"),
    path('charts/', stat_views.view_charts, name='charts'),
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

