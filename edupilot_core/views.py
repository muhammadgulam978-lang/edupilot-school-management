# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.views.decorators.csrf import csrf_protect

# @csrf_protect
# def login_view(request):
#     if request.user.is_authenticated:
#         if request.user.role == 'admin': return redirect('admin_dashboard')
#         elif request.user.role == 'teacher': return redirect('teacher_dashboard')
#         elif request.user.role == 'student': return redirect('student_dashboard')
#         else: return redirect('parent_dashboard')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         selected_role = request.POST.get('role')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             if user.role == selected_role:
#                 login(request, user)
#                 if user.role == 'admin': return redirect('admin_dashboard')
#                 elif user.role == 'teacher': return redirect('teacher_dashboard')
#                 elif user.role == 'student': return redirect('student_dashboard')
#                 else: return redirect('parent_dashboard')
#             else:
#                 messages.error(request, f"Access denied! Aapka role '{user.role}' hai.")
#         else:
#             messages.error(request, "Invalid username ya password.")
            
#     return render(request, 'login.html')

# def admin_dashboard_view(request):
#     return render(request, 'dashboard.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')
#


#after data analysis and financial KPIs addition 
   
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Sum
# from django.views.decorators.csrf import csrf_protect
# from .models import Student, Transaction

# @csrf_protect
# def login_view(request):
#     if request.user.is_authenticated:
#         if request.user.role == 'admin': return redirect('admin_dashboard')
#         elif request.user.role == 'teacher': return redirect('teacher_dashboard')
#         elif request.user.role == 'student': return redirect('student_dashboard')
#         else: return redirect('parent_dashboard')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         selected_role = request.POST.get('role')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             if user.role == selected_role:
#                 login(request, user)
#                 if user.role == 'admin': return redirect('admin_dashboard')
#                 elif user.role == 'teacher': return redirect('teacher_dashboard')
#                 elif user.role == 'student': return redirect('student_dashboard')
#                 else: return redirect('parent_dashboard')
#             else:
#                 messages.error(request, f"Access denied! Aapka role '{user.role}' hai.")
#         else:
#             messages.error(request, "Invalid username ya password.")
            
#     return render(request, 'login.html')

# @login_required(login_url='login')
# def admin_dashboard_view(request):
#     # Financial KPI Calculations
#     total_students = Student.objects.filter(is_active=True).count()
#     total_collected_fees = Student.objects.aggregate(Sum('fee_paid'))['fee_paid__sum'] or 0
#     total_outstanding_fees = Student.objects.aggregate(Sum('fee_due'))['fee_due__sum'] or 0
    
#     total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
#     total_expenses = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
#     net_profit = total_income - total_expenses
    
#     # Recent Transactions
#     recent_transactions = Transaction.objects.all().order_by('-date')[:5]

#     context = {
#         'total_students': total_students,
#         'total_collected_fees': total_collected_fees,
#         'total_outstanding_fees': total_outstanding_fees,
#         'net_profit': net_profit,
#         'recent_transactions': recent_transactions,
#     }
#     return render(request, 'dashboard.html', context)

# def logout_view(request):
#     logout(request)
#     return redirect('login')


# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Sum
# from django.views.decorators.csrf import csrf_protect
# from datetime import date
# from .models import Student, Transaction

# @csrf_protect
# def login_view(request):
#     if request.user.is_authenticated:
#         if request.user.role == 'admin': return redirect('admin_dashboard')
#         elif request.user.role == 'teacher': return redirect('teacher_dashboard')
#         elif request.user.role == 'student': return redirect('student_dashboard')
#         else: return redirect('parent_dashboard')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         selected_role = request.POST.get('role')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             if user.role == selected_role:
#                 login(request, user)
#                 if user.role == 'admin': return redirect('admin_dashboard')
#                 elif user.role == 'teacher': return redirect('teacher_dashboard')
#                 elif user.role == 'student': return redirect('student_dashboard')
#                 else: return redirect('parent_dashboard')
#             else:
#                 messages.error(request, f"Access denied! Aapka role '{user.role}' hai.")
#         else:
#             messages.error(request, "Invalid username ya password.")
            
#     return render(request, 'login.html')

# @login_required(login_url='login')
# def admin_dashboard_view(request):
#     # Financial KPI Calculations
#     total_students = Student.objects.filter(is_active=True).count()
#     total_collected_fees = Student.objects.aggregate(Sum('fee_paid'))['fee_paid__sum'] or 0
#     total_outstanding_fees = Student.objects.aggregate(Sum('fee_due'))['fee_due__sum'] or 0
    
#     # New Metrics with Category support
#     curr_month = date.today().month
#     monthly_revenue = Transaction.objects.filter(type='income', date__month=curr_month).aggregate(Sum('amount'))['amount__sum'] or 0
#     total_salaries = Transaction.objects.filter(type='expense', category='salary').aggregate(Sum('amount'))['amount__sum'] or 0
#     defaulter_count = Student.objects.filter(fee_due__gt=0).count()
    
#     # Collection %
#     total_due_potential = total_collected_fees + total_outstanding_fees
#     collection_percentage = (total_collected_fees / total_due_potential * 100) if total_due_potential > 0 else 0

#     # Basic Profit Logic
#     total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
#     total_expenses = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
#     net_profit = total_income - total_expenses
    
#     # Recent Transactions
#     recent_transactions = Transaction.objects.all().order_by('-date')[:5]

#     context = {
#         'total_students': total_students,
#         'total_collected_fees': total_collected_fees,
#         'total_outstanding_fees': total_outstanding_fees,
#         'net_profit': net_profit,
#         'monthly_revenue': monthly_revenue,
#         'total_salaries': total_salaries,
#         'defaulter_count': defaulter_count,
#         'collection_percentage': round(collection_percentage, 2),
#         'recent_transactions': recent_transactions,
#     }
#     return render(request, 'dashboard.html', context)

# def logout_view(request):
#     logout(request)
#     return redirect('login')


# with teachers

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect
from datetime import date
from .models import Student, Transaction, Teacher, Staff

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin': return redirect('admin_dashboard')
        elif request.user.role == 'teacher': return redirect('teacher_dashboard')
        elif request.user.role == 'student': return redirect('student_dashboard')
        else: return redirect('parent_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == selected_role:
                login(request, user)
                if user.role == 'admin': return redirect('admin_dashboard')
                elif user.role == 'teacher': return redirect('teacher_dashboard')
                elif user.role == 'student': return redirect('student_dashboard')
                else: return redirect('parent_dashboard')
            else: messages.error(request, f"Access denied! Aapka role '{user.role}' hai.")
        else: messages.error(request, "Invalid username ya password.")
    return render(request, 'login.html')

@login_required(login_url='login')
def admin_dashboard_view(request):
    total_students = Student.objects.filter(is_active=True).count()
    total_collected_fees = Student.objects.aggregate(Sum('fee_paid'))['fee_paid__sum'] or 0
    total_outstanding_fees = Student.objects.aggregate(Sum('fee_due'))['fee_due__sum'] or 0
    
    curr_month = date.today().month
    monthly_revenue = Transaction.objects.filter(type='income', date__month=curr_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_salaries = Transaction.objects.filter(type='expense', category='salary').aggregate(Sum('amount'))['amount__sum'] or 0
    defaulter_count = Student.objects.filter(fee_due__gt=0).count()
    
    total_due_potential = total_collected_fees + total_outstanding_fees
    collection_percentage = (total_collected_fees / total_due_potential * 100) if total_due_potential > 0 else 0
    
    total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_profit = total_income - total_expenses
    
    # Naye stats
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_staff = Staff.objects.filter(is_active=True).count()

    recent_transactions = Transaction.objects.all().order_by('-date')[:5]

    context = {
        'total_students': total_students, 'total_collected_fees': total_collected_fees,
        'total_outstanding_fees': total_outstanding_fees, 'net_profit': net_profit,
        'monthly_revenue': monthly_revenue, 'total_salaries': total_salaries,
        'defaulter_count': defaulter_count, 'collection_percentage': round(collection_percentage, 2),
        'recent_transactions': recent_transactions,
        'total_teachers': total_teachers, 'total_staff': total_staff,
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')