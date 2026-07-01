
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Sum
# from django.views.decorators.csrf import csrf_protect
# from datetime import date
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Student, Transaction, Teacher, Staff, StudentPerformance, FeeVoucher, AutomationJobDetail, get_dashboard_stats
# from .forms import StudentRegistrationForm
# from .services import FeeGenerationService

# # --- LOGIN/LOGOUT ---
# @csrf_protect
# def login_view(request):
#     if request.user.is_authenticated:
#         # User pehle se authenticated hai toh role ke mutabiq redirect karein
#         if request.user.role == 'admin': return redirect('admin_dashboard')
#         elif request.user.role == 'student': return redirect('student-dashboard')
#         elif request.user.role == 'parent': return redirect('parent-dashboard')
    
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         role = request.POST.get('role') # UI dropdown se milne wala role
        
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # Simple validation: user ka role check karein
#             if user.role.lower() == role:
#                 login(request, user)
#                 if role == 'admin': return redirect('admin_dashboard')
#                 elif role == 'student': return redirect('student-dashboard')
#                 elif role == 'parent': return redirect('parent-dashboard')
#                 else: return redirect('admin_dashboard') # Default fallback
#             else:
#                 messages.error(request, f"Invalid login for {role.upper()} portal.")
#         else:
#             messages.error(request, "Invalid username ya password.")
#     return render(request, 'login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# # --- ADMIN DASHBOARD ---
# @login_required(login_url='login')
# def admin_dashboard_view(request):
#     # Ab hum models.py mein banaye gaye helper function se stats utha rahe hain
#     context = get_dashboard_stats()
#     return render(request, 'dashboard.html', context)

# # API for Admin Dashboard (Dynamic Front-end ke liye)
# class AdminDashboardAPI(APIView):
#     def get(self, request):
#         data = get_dashboard_stats()
#         # API response format
#         return Response({
#             "stats": {
#                 "total_students": data['total_students'],
#                 "monthly_revenue": data['monthly_revenue'],
#                 "total_expenses": data['total_expenses'],
#                 "high_risk_students": data['high_risk_students'],
#                 "total_teachers": data['total_teachers'],
#                 "total_staff": data['total_staff']
#             },
#             "recent_transactions": list(data['recent_transactions'].values('title', 'amount', 'type', 'date'))
#         })

# # --- STUDENT & PARENT VIEWS ---
# def student_registration_view(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')
#     else:
#         form = StudentRegistrationForm()
#     return render(request, 'register.html', {'form': form})

# def generate_fees_view(request):
#     # Current month aur year nikal kar service call karna
#     today = date.today()
#     month_name = today.strftime("%B")
#     year = today.year
    
#     count = FeeGenerationService.generate_monthly_fees(month_name, year)
#     messages.success(request, f"{count} vouchers generated successfully for {month_name}-{year}!")
#     return redirect('/admin/edupilot_core/feevoucher/')

# @login_required
# def student_dashboard(request):
#     try:
#         if request.user.is_staff:
#              return render(request, 'student/dashboard.html', {'current_fee': {'amount': 'Admin Access', 'status': 'N/A'}})
             
#         voucher = FeeVoucher.objects.filter(student__admission_number=request.user.username).order_by('-id').first()
#         context = {
#             'current_fee': {
#                 'amount': voucher.net_amount if voucher else "No Voucher", # Fixed attribute
#                 'status': voucher.status if voucher else "N/A"
#             }
#         }
#     except:
#         context = {'current_fee': {'amount': "No Data", 'status': "N/A"}}
#     return render(request, 'student/dashboard.html', context)

# @login_required
# def parent_dashboard(request):
#     context = {'children': [], 'vouchers': []}
#     return render(request, 'parent/dashboard.html', context)

# def automation_logs(request):
#     logs = AutomationJobDetail.objects.all().order_by('-id')
#     return render(request, 'automation/logs.html', {'logs': logs})


# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Sum
# from django.views.decorators.csrf import csrf_protect
# from datetime import date
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Student, Transaction, Teacher, Staff, StudentPerformance, FeeVoucher, AutomationJobDetail, get_dashboard_stats, StudentBalance
# from .forms import StudentRegistrationForm
# from .services import FeeGenerationService

# # --- LOGIN/LOGOUT ---
# @csrf_protect
# def login_view(request):
#     if request.user.is_authenticated:
#         # User pehle se authenticated hai toh role ke mutabiq redirect karein
#         if request.user.role == 'admin': return redirect('admin_dashboard')
#         elif request.user.role == 'student': return redirect('student-dashboard')
#         elif request.user.role == 'parent': return redirect('parent-dashboard')
    
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         role = request.POST.get('role') # UI dropdown se milne wala role
        
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # Simple validation: user ka role check karein
#             if user.role.lower() == role:
#                 login(request, user)
#                 if role == 'admin': return redirect('admin_dashboard')
#                 elif role == 'student': return redirect('student-dashboard')
#                 elif role == 'parent': return redirect('parent-dashboard')
#                 else: return redirect('admin_dashboard') # Default fallback
#             else:
#                 messages.error(request, f"Invalid login for {role.upper()} portal.")
#         else:
#             messages.error(request, "Invalid username ya password.")
#     return render(request, 'login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# # --- ADMIN DASHBOARD ---
# @login_required(login_url='login')
# def admin_dashboard_view(request):
#     # Ab hum models.py mein banaye gaye helper function se stats utha rahe hain
#     context = get_dashboard_stats()
#     return render(request, 'dashboard.html', context)

# # API for Admin Dashboard (Dynamic Front-end ke liye)
# class AdminDashboardAPI(APIView):
#     def get(self, request):
#         data = get_dashboard_stats()
#         # API response format
#         return Response({
#             "stats": {
#                 "total_students": data['total_students'],
#                 "monthly_revenue": data['monthly_revenue'],
#                 "total_expenses": data['total_expenses'],
#                 "high_risk_students": data['high_risk_students'],
#                 "total_teachers": data['total_teachers'],
#                 "total_staff": data['total_staff']
#             },
#             "recent_transactions": list(data['recent_transactions'].values('title', 'amount', 'type', 'date'))
#         })

# # --- STUDENT & PARENT VIEWS ---
# def student_registration_view(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')
#     else:
#         form = StudentRegistrationForm()
#     return render(request, 'register.html', {'form': form})

# def generate_fees_view(request):
#     # Current month aur year nikal kar service call karna
#     today = date.today()
#     month_name = today.strftime("%B")
#     year = today.year
    
#     count = FeeGenerationService.generate_monthly_fees(month_name, year)
#     messages.success(request, f"{count} vouchers generated successfully for {month_name}-{year}!")
#     return redirect('/admin/edupilot_core/feevoucher/')

# @login_required
# @login_required
# def student_dashboard(request):
#     try:
#         student = Student.objects.get(admission_number=request.user.username)
#         vouchers = FeeVoucher.objects.filter(student=student).order_by('-id')
#         balance = StudentBalance.objects.get(student=student)
        
#         # ✅ GET NOTIFICATIONS
#         from .models import NotificationQueue
#         notifications = NotificationQueue.objects.filter(student=student).order_by('-created_at')[:10]
        
#         context = {
#             'student': student,
#             'vouchers': vouchers,
#             'balance': balance,
#             'notifications': notifications  # ← ADD YE
#         }
#     except:
#         context = {
#             'student': None,
#             'vouchers': [],
#             'balance': None,
#             'notifications': [],
#             'error': 'Student data not found'
#         }
#     return render(request, 'student_profile/dashboard.html', context)

# @login_required
# def parent_dashboard(request):
#     context = {'children': [], 'vouchers': []}
#     return render(request, 'parent/dashboard.html', context)

# def automation_logs(request):
#     logs = AutomationJobDetail.objects.all().order_by('-id')
#     return render(request, 'automation/logs.html', {'logs': logs})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, Transaction, Teacher, Staff, StudentPerformance, FeeVoucher, AutomationJobDetail, get_dashboard_stats, StudentBalance, NotificationQueue, SalaryVoucher
from .forms import StudentRegistrationForm
from .services import FeeGenerationService

# --- LOGIN/LOGOUT ---
@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        # User pehle se authenticated hai toh role ke mutabiq redirect karein
        if request.user.role == 'admin': return redirect('admin_dashboard')
        elif request.user.role == 'student': return redirect('student-dashboard')
        elif request.user.role == 'teacher': return redirect('teacher-dashboard')
        elif request.user.role == 'parent': return redirect('parent-dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role') # UI dropdown se milne wala role
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Simple validation: user ka role check karein
            if user.role.lower() == role:
                login(request, user)
                if role == 'admin': return redirect('admin_dashboard')
                elif role == 'student': return redirect('student-dashboard')
                elif role == 'teacher': return redirect('teacher-dashboard')
                elif role == 'parent': return redirect('parent-dashboard')
                else: return redirect('admin_dashboard') # Default fallback
            else:
                messages.error(request, f"Invalid login for {role.upper()} portal.")
        else:
            messages.error(request, "Invalid username ya password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- ADMIN DASHBOARD ---
@login_required(login_url='login')
def admin_dashboard_view(request):
    # Ab hum models.py mein banaye gaye helper function se stats utha rahe hain
    context = get_dashboard_stats()
    return render(request, 'dashboard.html', context)

# API for Admin Dashboard (Dynamic Front-end ke liye)
class AdminDashboardAPI(APIView):
    def get(self, request):
        data = get_dashboard_stats()
        # API response format
        return Response({
            "stats": {
                "total_students": data['total_students'],
                "monthly_revenue": data['monthly_revenue'],
                "total_expenses": data['total_expenses'],
                "high_risk_students": data['high_risk_students'],
                "total_teachers": data['total_teachers'],
                "total_staff": data['total_staff']
            },
            "recent_transactions": list(data['recent_transactions'].values('title', 'amount', 'type', 'date'))
        })

# --- STUDENT & PARENT VIEWS ---
def student_registration_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

def generate_fees_view(request):
    # Current month aur year nikal kar service call karna
    today = date.today()
    month_name = today.strftime("%B")
    year = today.year
    
    count = FeeGenerationService.generate_monthly_fees(month_name, year)
    messages.success(request, f"{count} vouchers generated successfully for {month_name}-{year}!")
    return redirect('/admin/edupilot_core/feevoucher/')

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(admission_number=request.user.username)
        vouchers = FeeVoucher.objects.filter(student=student).order_by('-id')
        balance = StudentBalance.objects.get(student=student)
        
        # ✅ GET NOTIFICATIONS
        notifications = NotificationQueue.objects.filter(student=student).order_by('-created_at')[:10]
        
        context = {
            'student': student,
            'vouchers': vouchers,
            'balance': balance,
            'notifications': notifications  # ← ADD YE
        }
    except:
        context = {
            'student': None,
            'vouchers': [],
            'balance': None,
            'notifications': [],
            'error': 'Student data not found'
        }
    return render(request, 'student_profile/dashboard.html', context)

@login_required
def teacher_dashboard(request):
    try:
        # Teacher model mein 'user' field nahi hai
        # Username ko teacher_id se match karo
        teacher = Teacher.objects.get(teacher_id=request.user.username)
        
        # Get salary vouchers
        salary_vouchers = SalaryVoucher.objects.filter(teacher=teacher).order_by('-id')
        
        # Get notifications (empty - teacher notifications not in system)
        notifications = []
        
        context = {
            'teacher': teacher,
            'salary_vouchers': salary_vouchers,
            'notifications': notifications
        }
    except Teacher.DoesNotExist:
        context = {
            'teacher': None,
            'salary_vouchers': [],
            'notifications': [],
            'error': 'Teacher record not found'
        }
    except Exception as e:
        context = {
            'teacher': None,
            'salary_vouchers': [],
            'notifications': [],
            'error': f'Error: {str(e)}'
        }
    
    return render(request, 'teacher_dashboard/teacher_dashboard.html', context)

@login_required
def parent_dashboard(request):
    context = {'children': [], 'vouchers': []}
    return render(request, 'parent/dashboard.html', context)

def automation_logs(request):
    logs = AutomationJobDetail.objects.all().order_by('-id')
    return render(request, 'automation/logs.html', {'logs': logs})