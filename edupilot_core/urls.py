# from django.contrib import admin
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('login/', views.login_view, name='login'),
#     # 
#     path('logout/', views.logout_view, name='logout'),
#     path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
#     path('register-student/', views.student_registration_view, name='register_student'),
# ]

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('register-student/', views.student_registration_view, name='register_student'),
    
    # Ye path button ke liye hai
    path('admin/edupilot_core/feevoucher/generate-all-fees/', views.generate_fees_view, name='generate_fees_view'),
]

# Media files serving (Browser mein PDF dekhne/download karne ke liye)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)