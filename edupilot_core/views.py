
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect
from datetime import date
from .models import Student, Transaction, Teacher, Staff, StudentPerformance 
from .forms import StudentRegistrationForm

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username ya password.")
    return render(request, 'login.html')

@login_required(login_url='login')
def admin_dashboard_view(request):
    # Stats ke liye ab sirf wahi fields use ho rahi hain jo aapke model mein hain
    total_students = Student.objects.filter(is_active=True).count()
    
    curr_month = date.today().month
    monthly_revenue = Transaction.objects.filter(type='income', date__month=curr_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_staff = Staff.objects.filter(is_active=True).count()
    
    high_risk_students = StudentPerformance.objects.filter(risk_level='High').count()
    recent_transactions = Transaction.objects.all().order_by('-date')[:5]

    context = {
        'total_students': total_students,
        'monthly_revenue': monthly_revenue,
        'total_expenses': total_expenses,
        'total_teachers': total_teachers, 
        'total_staff': total_staff,
        'recent_transactions': recent_transactions,
        'high_risk_students': high_risk_students,
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def student_registration_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import redirect
from django.contrib import messages
from .services import FeeGenerationService

def generate_fees_view(request):
    # June 2026 ke liye generate kar rahe hain (aap isay dynamic bhi kar sakte hain)
    count = FeeGenerationService.generate_monthly_fees("June-2026")
    messages.success(request, f"{count} vouchers generated successfully!")
    return redirect('/admin/edupilot_core/feevoucher/')