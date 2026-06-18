from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]