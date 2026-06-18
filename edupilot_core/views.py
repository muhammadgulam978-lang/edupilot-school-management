from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    # Agar user pehle se logged in hai, toh use direct dashboard bhejo
    if request.user.is_authenticated:
        if request.user.role == 'admin': return redirect('admin_dashboard')
        elif request.user.role == 'teacher': return redirect('teacher_dashboard')
        elif request.user.role == 'student': return redirect('student_dashboard')
        else: return redirect('parent_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')

        # 1. User authenticate karein
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 2. Role check karein
            if user.role == selected_role:
                login(request, user)
                
                # 3. Role ke mutabiq redirect
                if user.role == 'admin': return redirect('admin_dashboard')
                elif user.role == 'teacher': return redirect('teacher_dashboard')
                elif user.role == 'student': return redirect('student_dashboard')
                else: return redirect('parent_dashboard')
            else:
                messages.error(request, f"Access denied! Aapka role '{user.role}' hai, par aapne '{selected_role}' chuna hai.")
        else:
            messages.error(request, "Invalid username ya password.")
            
    return render(request, 'login.html')

def admin_dashboard_view(request):
    return render(request, 'dashboard.html')