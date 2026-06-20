

# from django.contrib import admin
# from .models import User, Student, Transaction, Teacher, Staff, StudentPerformance

# admin.site.register(User)

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     # Nayi fields jo aapne registration form ke liye define ki thin
#     list_display = ('full_name', 'admission_number', 'admission_date', 'current_class', 'is_active')
#     search_fields = ('full_name', 'admission_number', 'student_id')
#     list_filter = ('is_active', 'campus', 'current_class')

# @admin.register(StudentPerformance)
# class StudentPerformanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'attendance_percentage', 'average_test_score', 'risk_level')
#     list_filter = ('risk_level',)
#     search_fields = ('student__full_name',) # 'name' ki jagah 'full_name'

# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'amount', 'type', 'date')
#     list_filter = ('type', 'date')

# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('name', 'employee_id', 'is_active')
#     search_fields = ('name', 'employee_id')
#     list_filter = ('is_active',)

# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('name', 'role', 'is_active')
#     search_fields = ('name', 'role')
#     list_filter = ('is_active', 'role')


# from django.contrib import admin
# from .models import User, Student, Transaction, Teacher, Staff, StudentPerformance, FeeHead

# # Registering User
# admin.site.register(User)

# # Student Admin
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'admission_number', 'admission_date', 'current_class', 'is_active')
#     search_fields = ('full_name', 'admission_number', 'student_id')
#     list_filter = ('is_active', 'campus', 'current_class')

# # Student Performance Admin
# @admin.register(StudentPerformance)
# class StudentPerformanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'attendance_percentage', 'average_test_score', 'risk_level')
#     list_filter = ('risk_level',)
#     search_fields = ('student__full_name',)

# # Transaction Admin
# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'amount', 'type', 'date')
#     list_filter = ('type', 'date')

# # Teacher Admin
# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('name', 'employee_id', 'is_active')
#     search_fields = ('name', 'employee_id')
#     list_filter = ('is_active',)

# # Staff Admin
# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('name', 'role', 'is_active')
#     search_fields = ('name', 'role')
#     list_filter = ('is_active', 'role')

# # Fee Head Admin (Phase 1 Integration)
# @admin.register(FeeHead)
# class FeeHeadAdmin(admin.ModelAdmin):
#     list_display = ('name', 'frequency', 'status')
#     list_filter = ('frequency', 'status')
#     search_fields = ('name',)


# from django.contrib import admin
# from .models import Scholarship, TransportRoute, User, Student, Transaction, Teacher, Staff, StudentPerformance, FeeHead, FeePlan, FeePlanDetail, StudentFeeAssignment

# # Registering User
# admin.site.register(User)

# # Student Admin
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'admission_number', 'admission_date', 'current_class', 'is_active')
#     search_fields = ('full_name', 'admission_number', 'student_id')
#     list_filter = ('is_active', 'campus', 'current_class')

# # Student Performance Admin
# @admin.register(StudentPerformance)
# class StudentPerformanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'attendance_percentage', 'average_test_score', 'risk_level')
#     list_filter = ('risk_level',)
#     search_fields = ('student__full_name',)

# # Transaction Admin
# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'amount', 'type', 'date')
#     list_filter = ('type', 'date')

# # Teacher Admin
# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('name', 'employee_id', 'is_active')
#     search_fields = ('name', 'employee_id')
#     list_filter = ('is_active',)

# # Staff Admin
# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('name', 'role', 'is_active')
#     search_fields = ('name', 'role')
#     list_filter = ('is_active', 'role')

# # Fee Head Admin (Phase 1)
# @admin.register(FeeHead)
# class FeeHeadAdmin(admin.ModelAdmin):
#     list_display = ('name', 'frequency', 'status')
#     list_filter = ('frequency', 'status')
#     search_fields = ('name',)

# # Fee Plan Admin (Phase 2)
# @admin.register(FeePlan)
# class FeePlanAdmin(admin.ModelAdmin):
#     list_display = ('name', 'class_name', 'session')
#     search_fields = ('name', 'class_name')

# @admin.register(FeePlanDetail)
# class FeePlanDetailAdmin(admin.ModelAdmin):
#     list_display = ('fee_plan', 'fee_head', 'amount')
#     list_filter = ('fee_plan', 'fee_head')

# # Transport Admin (Phase 3)
# @admin.register(TransportRoute)
# class TransportRouteAdmin(admin.ModelAdmin):
#     list_display = ('route_name', 'amount')

# # Scholarship Admin (Phase 4)
# @admin.register(Scholarship)
# class ScholarshipAdmin(admin.ModelAdmin):
#     list_display = ('name', 'discount_type', 'value')

# # Student Fee Assignment Admin (Phase 5)
# @admin.register(StudentFeeAssignment)
# class StudentFeeAssignmentAdmin(admin.ModelAdmin):
#     list_display = ('student', 'fee_plan', 'transport_route', 'scholarship')
#     list_filter = ('fee_plan', 'transport_route')
#     search_fields = ('student__full_name',)


# phase 7

# from django.contrib import admin
# from .models import (
#     Scholarship, TransportRoute, User, Student, Transaction, Teacher, Staff, 
#     StudentPerformance, FeeHead, FeePlan, FeePlanDetail, StudentFeeAssignment,
#     StudentLedger, StudentBalance, FeeVoucher, FeeVoucherItem
# )

# # Registering User
# admin.site.register(User)

# # Student Admin
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'admission_number', 'admission_date', 'current_class', 'is_active')
#     search_fields = ('full_name', 'admission_number', 'student_id')
#     list_filter = ('is_active', 'campus', 'current_class')

# # Student Performance Admin
# @admin.register(StudentPerformance)
# class StudentPerformanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'attendance_percentage', 'average_test_score', 'risk_level')
#     list_filter = ('risk_level',)
#     search_fields = ('student__full_name',)

# # Transaction Admin
# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'amount', 'type', 'date')
#     list_filter = ('type', 'date')

# # Teacher Admin
# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('name', 'employee_id', 'is_active')
#     search_fields = ('name', 'employee_id')
#     list_filter = ('is_active',)

# # Staff Admin
# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('name', 'role', 'is_active')
#     search_fields = ('name', 'role')
#     list_filter = ('is_active', 'role')

# # Fee Head Admin (Phase 1)
# @admin.register(FeeHead)
# class FeeHeadAdmin(admin.ModelAdmin):
#     list_display = ('name', 'frequency', 'status')
#     list_filter = ('frequency', 'status')
#     search_fields = ('name',)

# # Fee Plan Admin (Phase 2)
# @admin.register(FeePlan)
# class FeePlanAdmin(admin.ModelAdmin):
#     list_display = ('name', 'class_name', 'session')
#     search_fields = ('name', 'class_name')

# @admin.register(FeePlanDetail)
# class FeePlanDetailAdmin(admin.ModelAdmin):
#     list_display = ('fee_plan', 'fee_head', 'amount')
#     list_filter = ('fee_plan', 'fee_head')

# # Transport Admin (Phase 3)
# @admin.register(TransportRoute)
# class TransportRouteAdmin(admin.ModelAdmin):
#     list_display = ('route_name', 'amount')

# # Scholarship Admin (Phase 4)
# @admin.register(Scholarship)
# class ScholarshipAdmin(admin.ModelAdmin):
#     list_display = ('name', 'discount_type', 'value')

# # Student Fee Assignment Admin (Phase 5)
# @admin.register(StudentFeeAssignment)
# class StudentFeeAssignmentAdmin(admin.ModelAdmin):
#     list_display = ('student', 'fee_plan', 'transport_route', 'scholarship')
#     list_filter = ('fee_plan', 'transport_route')
#     search_fields = ('student__full_name',)

# # Student Ledger Admin (Phase 6)
# @admin.register(StudentLedger)
# class StudentLedgerAdmin(admin.ModelAdmin):
#     list_display = ('student', 'date', 'description', 'debit', 'credit', 'balance')
#     list_filter = ('student', 'date')
#     search_fields = ('student__full_name',)

# # Student Balance Admin (Phase 7)
# @admin.register(StudentBalance)
# class StudentBalanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'outstanding_amount')
#     search_fields = ('student__full_name',)

# # Fee Voucher Admin (Phase 8)
# class FeeVoucherItemInline(admin.TabularInline):
#     model = FeeVoucherItem
#     extra = 1

# @admin.register(FeeVoucher)
# class FeeVoucherAdmin(admin.ModelAdmin):
#     list_display = ('voucher_no', 'student', 'month', 'net_amount', 'status')
#     list_filter = ('status', 'month')
#     search_fields = ('voucher_no', 'student__full_name')
#     inlines = [FeeVoucherItemInline]

# # Fee Voucher Item Admin (Phase 9)
# @admin.register(FeeVoucherItem)
# class FeeVoucherItemAdmin(admin.ModelAdmin):
#     list_display = ('voucher', 'fee_head', 'amount')
#     list_filter = ('voucher',)


# phase 10: Fee Generation Service Integration

# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import redirect
# from django.contrib import messages
# from .services import FeeGenerationService
# from .models import (
#     Scholarship, TransportRoute, User, Student, Transaction, Teacher, Staff, 
#     StudentPerformance, FeeHead, FeePlan, FeePlanDetail, StudentFeeAssignment,
#     StudentLedger, StudentBalance, FeeVoucher, FeeVoucherItem
# )

# # Registering User
# admin.site.register(User)

# # Student Admin
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'admission_number', 'admission_date', 'current_class', 'is_active')
#     search_fields = ('full_name', 'admission_number', 'student_id')
#     list_filter = ('is_active', 'campus', 'current_class')

# # Student Performance Admin
# @admin.register(StudentPerformance)
# class StudentPerformanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'attendance_percentage', 'average_test_score', 'risk_level')
#     list_filter = ('risk_level',)
#     search_fields = ('student__full_name',)

# # Transaction Admin
# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'amount', 'type', 'date')
#     list_filter = ('type', 'date')

# # Teacher Admin
# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('name', 'employee_id', 'is_active')
#     search_fields = ('name', 'employee_id')
#     list_filter = ('is_active',)

# # Staff Admin
# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ('name', 'role', 'is_active')
#     search_fields = ('name', 'role')
#     list_filter = ('is_active', 'role')

# # Fee Head Admin (Phase 1)
# @admin.register(FeeHead)
# class FeeHeadAdmin(admin.ModelAdmin):
#     list_display = ('name', 'frequency', 'status')
#     list_filter = ('frequency', 'status')
#     search_fields = ('name',)

# # Fee Plan Admin (Phase 2)
# @admin.register(FeePlan)
# class FeePlanAdmin(admin.ModelAdmin):
#     list_display = ('name', 'class_name', 'session')
#     search_fields = ('name', 'class_name')

# @admin.register(FeePlanDetail)
# class FeePlanDetailAdmin(admin.ModelAdmin):
#     list_display = ('fee_plan', 'fee_head', 'amount')
#     list_filter = ('fee_plan', 'fee_head')

# # Transport Admin (Phase 3)
# @admin.register(TransportRoute)
# class TransportRouteAdmin(admin.ModelAdmin):
#     list_display = ('route_name', 'amount')

# # Scholarship Admin (Phase 4)
# @admin.register(Scholarship)
# class ScholarshipAdmin(admin.ModelAdmin):
#     list_display = ('name', 'discount_type', 'value')

# # Student Fee Assignment Admin (Phase 5)
# @admin.register(StudentFeeAssignment)
# class StudentFeeAssignmentAdmin(admin.ModelAdmin):
#     list_display = ('student', 'fee_plan', 'transport_route', 'scholarship')
#     list_filter = ('fee_plan', 'transport_route')
#     search_fields = ('student__full_name',)

# # Student Ledger Admin (Phase 6)
# @admin.register(StudentLedger)
# class StudentLedgerAdmin(admin.ModelAdmin):
#     list_display = ('student', 'date', 'description', 'debit', 'credit', 'balance')
#     list_filter = ('student', 'date')
#     search_fields = ('student__full_name',)

# # Student Balance Admin (Phase 7)
# @admin.register(StudentBalance)
# class StudentBalanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'outstanding_amount')
#     search_fields = ('student__full_name',)

# # Fee Voucher Admin (Phase 8)
# class FeeVoucherItemInline(admin.TabularInline):
#     model = FeeVoucherItem
#     extra = 1

# @admin.register(FeeVoucher)
# class FeeVoucherAdmin(admin.ModelAdmin):
#     list_display = ('voucher_no', 'student', 'month', 'net_amount', 'status')
#     list_filter = ('status', 'month')
#     search_fields = ('voucher_no', 'student__full_name')
#     inlines = [FeeVoucherItemInline]
    
#     # Custom Template for Button
#     change_list_template = "fee_voucher_change_list.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('generate-all-fees/', self.admin_site.admin_view(self.generate_fees_view), name='generate_all_fees'),
#         ]
#         return my_urls + urls

#     def generate_fees_view(self, request):
#         # Yahan hum current month hardcode kar rahe hain, aap ise dynamic bhi kar sakte hain
#         from datetime import datetime
#         month = datetime.now().strftime("%B-%Y")
        
#         count = FeeGenerationService.generate_monthly_fees(month)
#         messages.success(request, f"{count} Vouchers generated successfully!")
#         return redirect('..')

# # Fee Voucher Item Admin (Phase 9)
# @admin.register(FeeVoucherItem)
# class FeeVoucherItemAdmin(admin.ModelAdmin):
#     list_display = ('voucher', 'fee_head', 'amount')
#     list_filter = ('voucher',)


# email service
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime
from .services import FeeGenerationService
from .models import (
    Scholarship, TransportRoute, User, Student, Transaction, Teacher, Staff, 
    StudentPerformance, FeeHead, FeePlan, FeePlanDetail, StudentFeeAssignment,
    StudentLedger, StudentBalance, FeeVoucher, FeeVoucherItem,
    FeeGenerationSettings, NotificationQueue, FeeGenerationLog
)

# Registering User
admin.site.register(User)

# Automation Settings Admin
@admin.register(FeeGenerationSettings)
class FeeGenerationSettingsAdmin(admin.ModelAdmin):
    list_display = ('auto_enabled', 'generation_day', 'generation_time', 'send_notifications')

# Notification Queue Admin
@admin.register(NotificationQueue)
class NotificationQueueAdmin(admin.ModelAdmin):
    list_display = ('student', 'notification_type', 'status', 'created_at')
    list_filter = ('status', 'notification_type', 'created_at')
    search_fields = ('student__full_name',)

# Generation Logs Admin (Phase 7)
@admin.register(FeeGenerationLog)
class FeeGenerationLogAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'status', 'students_processed', 'success_count', 'failed_count', 'started_at')
    list_filter = ('status', 'month', 'year')

# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'admission_number', 'admission_date', 'current_class', 'is_active')
    search_fields = ('full_name', 'admission_number', 'student_id')
    list_filter = ('is_active', 'campus', 'current_class')

# Student Performance Admin
@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'attendance_percentage', 'average_test_score', 'risk_level')
    list_filter = ('risk_level',)
    search_fields = ('student__full_name',)

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'type', 'date')
    list_filter = ('type', 'date')

# Teacher & Staff Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'is_active')
    search_fields = ('name', 'employee_id')
    list_filter = ('is_active',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active')
    search_fields = ('name', 'role')
    list_filter = ('is_active', 'role')

# Fee Head & Plan Admin
@admin.register(FeeHead)
class FeeHeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'frequency', 'status')
    list_filter = ('frequency', 'status')
    search_fields = ('name',)

@admin.register(FeePlan)
class FeePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'session')
    search_fields = ('name', 'class_name')

@admin.register(FeePlanDetail)
class FeePlanDetailAdmin(admin.ModelAdmin):
    list_display = ('fee_plan', 'fee_head', 'amount')
    list_filter = ('fee_plan', 'fee_head')

# Transport & Scholarship Admin
@admin.register(TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'amount')

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_type', 'value')

# Student Fee Assignment & Ledger Admin
@admin.register(StudentFeeAssignment)
class StudentFeeAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_plan', 'transport_route', 'scholarship')
    list_filter = ('fee_plan', 'transport_route')
    search_fields = ('student__full_name',)

@admin.register(StudentLedger)
class StudentLedgerAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'description', 'debit', 'credit', 'balance')
    list_filter = ('student', 'date')
    search_fields = ('student__full_name',)

@admin.register(StudentBalance)
class StudentBalanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'outstanding_amount')
    search_fields = ('student__full_name',)

# Fee Voucher Admin
class FeeVoucherItemInline(admin.TabularInline):
    model = FeeVoucherItem
    extra = 1

@admin.register(FeeVoucher)
class FeeVoucherAdmin(admin.ModelAdmin):
    list_display = ('voucher_no', 'student', 'month', 'net_amount', 'status')
    list_filter = ('status', 'month')
    search_fields = ('voucher_no', 'student__full_name')
    inlines = [FeeVoucherItemInline]
    
    change_list_template = "fee_voucher_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('generate-all-fees/', self.admin_site.admin_view(self.generate_fees_view), name='generate_all_fees'),
        ]
        return my_urls + urls

    def generate_fees_view(self, request):
        now = datetime.now()
        month = now.strftime("%B") # eg: June
        year = now.year            # eg: 2026
        
        # Service call with both arguments
        count = FeeGenerationService.generate_monthly_fees(month, year)
        
        messages.success(request, f"{count} Vouchers generated successfully for {month}-{year}!")
        return redirect('..')

@admin.register(FeeVoucherItem)
class FeeVoucherItemAdmin(admin.ModelAdmin):
    list_display = ('voucher', 'fee_head', 'amount')
    list_filter = ('voucher',)