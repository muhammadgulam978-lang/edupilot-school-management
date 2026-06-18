from django.contrib import admin
from .models import User, Student, Transaction, Teacher, Staff

# User model ko register karna
admin.site.register(User)

# Student model ko register karna
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'enrollment_number', 'fee_due', 'fee_paid', 'is_active')
    search_fields = ('name', 'enrollment_number')

# Transaction model ko register karna
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'type', 'date')
    list_filter = ('type', 'date')

# Teacher model ko register karna
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'is_active')
    search_fields = ('name', 'employee_id')
    list_filter = ('is_active',)

# Staff model ko register karna
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active')
    search_fields = ('name', 'role')
    list_filter = ('is_active', 'role')