
# from django.contrib import admin
# from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static

# # Import Views
# from . import views

# # Import APIs
# from .api.serializers import StudentDashboardAPI, ParentDashboardAPI
# from .views import AdminDashboardAPI 

# urlpatterns = [
#     path('admin/', admin.site.urls),
    
#     # Auth
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
    
#     # Dashboard Pages
#     path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
#     path('register-student/', views.student_registration_view, name='register_student'),
#     path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    
#     # Student/Parent/Automation Pages
#     path('parent/dashboard/', views.parent_dashboard, name='parent-dashboard'),
#     path('automation/logs/', views.automation_logs, name='automation-logs'),
    
#     # Automation Action
#     path('admin/edupilot_core/feevoucher/generate-all-fees/', views.generate_fees_view, name='generate_fees_view'),
    
#     # API Endpoints
#     path('api/student/dashboard/', StudentDashboardAPI.as_view(), name='student-dashboard-api'),
#     path('api/parent/dashboard/', ParentDashboardAPI.as_view(), name='parent-dashboard-api'),
#     path('api/admin/dashboard/', AdminDashboardAPI.as_view(), name='admin-dashboard-api'),
# ]

# # Media Files
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import Views
from . import views

# Import APIs
from .views import AdminDashboardAPI 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard Pages
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('register-student/', views.student_registration_view, name='register_student'),
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    
    # Student/Parent/Automation Pages
    path('parent/dashboard/', views.parent_dashboard, name='parent-dashboard'),
    path('automation/logs/', views.automation_logs, name='automation-logs'),
    
    # Automation Action
    path('admin/edupilot_core/feevoucher/generate-all-fees/', views.generate_fees_view, name='generate_fees_view'),
    
    # API Endpoints
    path('api/admin/dashboard/', AdminDashboardAPI.as_view(), name='admin-dashboard-api'),
]

# Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)