

# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models
# from django.utils import timezone # Ye import zaroor karein


# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     groups = models.ManyToManyField(
#         Group, verbose_name='groups', blank=True,
#         related_name="edupilot_user_set", related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission, verbose_name='user permissions', blank=True,
#         related_name="edupilot_user_permissions_set", related_query_name="user",
#     )


# from django.db import models

# class Student(models.Model):
#     # Basic Information
#     student_id = models.CharField(max_length=20, unique=True)
#     admission_number = models.CharField(max_length=20, unique=True)
#     full_name = models.CharField(max_length=100)
#     father_name = models.CharField(max_length=100)
#     mother_name = models.CharField(max_length=100)
#     cnic_bform = models.CharField(max_length=20)
#     date_of_birth = models.DateField()
#     class_name = models.CharField(max_length=20)
#     section = models.CharField(max_length=10)
#     campus = models.CharField(max_length=50)

#     # Contact Information
#     parent_mobile = models.CharField(max_length=15)
#     parent_email = models.EmailField()
#     home_address = models.TextField()

#     # Academic Information
#     admission_date = models.DateField()
#     current_class = models.CharField(max_length=20)
#     session = models.CharField(max_length=20)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.full_name

# class Transaction(models.Model):
#     TRANSACTION_TYPES = [('income', 'Income'), ('expense', 'Expense')]
#     CATEGORY_CHOICES = [('fee', 'Fee'), ('salary', 'Salary'), ('other', 'Other')]
#     title = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
#     category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.amount} ({self.type})"

# class Teacher(models.Model):
#     name = models.CharField(max_length=100)
#     employee_id = models.CharField(max_length=50, unique=True)
#     is_active = models.BooleanField(default=True)
#     def __str__(self): return self.name

# class Staff(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     def __str__(self): return self.name
#     # models.py mein naya model add karein
# from django.db import models
# # Assume k Student model isi app mein hai, agar dusri app mein hai toh wahan se import karein
# from .models import Student 

# class StudentPerformance(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE)
#     attendance_percentage = models.FloatField(default=0.0)
#     average_test_score = models.FloatField(default=0.0)
#     risk_level = models.CharField(max_length=20, default='Low')

#     def save(self, *args, **kwargs):
#         # AI Logic: Auto-calculate risk based on thresholds
#         if self.attendance_percentage < 50 or self.average_test_score < 40:
#             self.risk_level = 'High'
#         elif self.attendance_percentage < 75 or self.average_test_score < 65:
#             self.risk_level = 'Medium'
#         else:
#             self.risk_level = 'Low'
        
#         # Save the instance to the database
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student.name} - {self.risk_level} Risk"

# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models
# from django.utils import timezone

# # --- USER MODELS ---
# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     groups = models.ManyToManyField(
#         Group, verbose_name='groups', blank=True,
#         related_name="edupilot_user_set", related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission, verbose_name='user permissions', blank=True,
#         related_name="edupilot_user_permissions_set", related_query_name="user",
#     )

# # --- STUDENT & ACADEMIC MODELS ---
# class Student(models.Model):
#     student_id = models.CharField(max_length=20, unique=True)
#     admission_number = models.CharField(max_length=20, unique=True)
#     full_name = models.CharField(max_length=100)
#     father_name = models.CharField(max_length=100)
#     mother_name = models.CharField(max_length=100)
#     cnic_bform = models.CharField(max_length=20)
#     date_of_birth = models.DateField()
#     class_name = models.CharField(max_length=20)
#     section = models.CharField(max_length=10)
#     campus = models.CharField(max_length=50)
#     parent_mobile = models.CharField(max_length=15)
#     parent_email = models.EmailField()
#     home_address = models.TextField()
#     admission_date = models.DateField()
#     current_class = models.CharField(max_length=20)
#     session = models.CharField(max_length=20)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.full_name

# class StudentPerformance(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE)
#     attendance_percentage = models.FloatField(default=0.0)
#     average_test_score = models.FloatField(default=0.0)
#     risk_level = models.CharField(max_length=20, default='Low')

#     def save(self, *args, **kwargs):
#         if self.attendance_percentage < 50 or self.average_test_score < 40:
#             self.risk_level = 'High'
#         elif self.attendance_percentage < 75 or self.average_test_score < 65:
#             self.risk_level = 'Medium'
#         else:
#             self.risk_level = 'Low'
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student.full_name} - {self.risk_level} Risk"

# # --- STAFF & OTHER MODELS ---
# class Teacher(models.Model):
#     name = models.CharField(max_length=100)
#     employee_id = models.CharField(max_length=50, unique=True)
#     is_active = models.BooleanField(default=True)
#     def __str__(self): return self.name

# class Staff(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     def __str__(self): return self.name

# class Transaction(models.Model):
#     TRANSACTION_TYPES = [('income', 'Income'), ('expense', 'Expense')]
#     CATEGORY_CHOICES = [('fee', 'Fee'), ('salary', 'Salary'), ('other', 'Other')]
#     title = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
#     category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.amount} ({self.type})"

# # --- PHASE 1: FEE HEADS ---
# class FeeHead(models.Model):
#     FREQUENCY_CHOICES = [
#         ('one_time', 'One Time'),
#         ('monthly', 'Monthly'),
#         ('yearly', 'Yearly'),
#     ]
    
#     name = models.CharField(max_length=100)
#     frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
#     status = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.name} ({self.frequency})"

#     class Meta:
#         verbose_name = "Fee Head"
#         verbose_name_plural = "Fee Heads"

        

# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models
# from django.utils import timezone

# # --- USER MODELS ---
# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     groups = models.ManyToManyField(
#         Group, verbose_name='groups', blank=True,
#         related_name="edupilot_user_set", related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission, verbose_name='user permissions', blank=True,
#         related_name="edupilot_user_permissions_set", related_query_name="user",
#     )

# # --- STUDENT & ACADEMIC MODELS ---
# class Student(models.Model):
#     student_id = models.CharField(max_length=20, unique=True)
#     admission_number = models.CharField(max_length=20, unique=True)
#     full_name = models.CharField(max_length=100)
#     father_name = models.CharField(max_length=100)
#     mother_name = models.CharField(max_length=100)
#     cnic_bform = models.CharField(max_length=20)
#     date_of_birth = models.DateField()
#     class_name = models.CharField(max_length=20)
#     section = models.CharField(max_length=10)
#     campus = models.CharField(max_length=50)
#     parent_mobile = models.CharField(max_length=15)
#     parent_email = models.EmailField()
#     home_address = models.TextField()
#     admission_date = models.DateField()
#     current_class = models.CharField(max_length=20)
#     session = models.CharField(max_length=20)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.full_name

# class StudentPerformance(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE)
#     attendance_percentage = models.FloatField(default=0.0)
#     average_test_score = models.FloatField(default=0.0)
#     risk_level = models.CharField(max_length=20, default='Low')

#     def save(self, *args, **kwargs):
#         if self.attendance_percentage < 50 or self.average_test_score < 40:
#             self.risk_level = 'High'
#         elif self.attendance_percentage < 75 or self.average_test_score < 65:
#             self.risk_level = 'Medium'
#         else:
#             self.risk_level = 'Low'
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.student.full_name} - {self.risk_level} Risk"

# # --- STAFF & OTHER MODELS ---
# class Teacher(models.Model):
#     name = models.CharField(max_length=100)
#     employee_id = models.CharField(max_length=50, unique=True)
#     is_active = models.BooleanField(default=True)
#     def __str__(self): return self.name

# class Staff(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     def __str__(self): return self.name

# class Transaction(models.Model):
#     TRANSACTION_TYPES = [('income', 'Income'), ('expense', 'Expense')]
#     CATEGORY_CHOICES = [('fee', 'Fee'), ('salary', 'Salary'), ('other', 'Other')]
#     title = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
#     category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.amount} ({self.type})"

# # --- PHASE 1: FEE HEADS ---
# class FeeHead(models.Model):
#     FREQUENCY_CHOICES = [
#         ('one_time', 'One Time'),
#         ('monthly', 'Monthly'),
#         ('yearly', 'Yearly'),
#     ]
    
#     name = models.CharField(max_length=100)
#     frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
#     status = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.name} ({self.frequency})"

#     class Meta:
#         verbose_name = "Fee Head"
#         verbose_name_plural = "Fee Heads"

# # --- PHASE 2: CLASS FEE PLANS ---
# class FeePlan(models.Model):
#     name = models.CharField(max_length=100)
#     class_name = models.CharField(max_length=20)
#     session = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.name} ({self.class_name})"

# class FeePlanDetail(models.Model):
#     fee_plan = models.ForeignKey(FeePlan, on_delete=models.CASCADE, related_name='details')
#     fee_head = models.ForeignKey(FeeHead, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.fee_plan.name} - {self.fee_head.name}"
    

#     # --- PHASE 3: TRANSPORT MODULE ---
# class TransportRoute(models.Model):
#     route_name = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.route_name} - {self.amount}"

# # --- PHASE 4: SCHOLARSHIP / DISCOUNT MODULE ---
# class Scholarship(models.Model):
#     DISCOUNT_TYPES = [('percentage', 'Percentage'), ('fixed', 'Fixed Amount')]
#     name = models.CharField(max_length=100)
#     discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
#     value = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.name} ({self.discount_type})"
#     # --- PHASE 5: STUDENT FEE ASSIGNMENT ---
# class StudentFeeAssignment(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='fee_assignment')
#     fee_plan = models.ForeignKey(FeePlan, on_delete=models.PROTECT)
#     transport_route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, blank=True)
#     scholarship = models.ForeignKey(Scholarship, on_delete=models.SET_NULL, null=True, blank=True)
    
#     def __str__(self):
#         return f"{self.student.full_name} - {self.fee_plan.name}"



# phase 7

# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from decimal import Decimal

# # --- PHASE 0: CUSTOM USER MODEL ---
# class User(AbstractUser):
#     pass

# # --- PHASE 1: FEE HEADS ---
# class FeeHead(models.Model):
#     FREQUENCY_CHOICES = [('one_time', 'One Time'), ('monthly', 'Monthly'), ('yearly', 'Yearly')]
#     name = models.CharField(max_length=100)
#     frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
#     status = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.name} ({self.frequency})"

# # --- PHASE 2: FEE PLANS ---
# class FeePlan(models.Model):
#     name = models.CharField(max_length=100)
#     class_name = models.CharField(max_length=50)
#     session = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.name} - {self.class_name}"

# class FeePlanDetail(models.Model):
#     fee_plan = models.ForeignKey(FeePlan, on_delete=models.CASCADE)
#     fee_head = models.ForeignKey(FeeHead, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

# # --- PHASE 3: TRANSPORT ---
# class TransportRoute(models.Model):
#     route_name = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.route_name

# # --- PHASE 4: SCHOLARSHIP ---
# class Scholarship(models.Model):
#     DISCOUNT_TYPES = [('percentage', 'Percentage'), ('fixed', 'Fixed Amount')]
#     name = models.CharField(max_length=100)
#     discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
#     value = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.name

# # --- CORE MODELS ---
# class Student(models.Model):
#     full_name = models.CharField(max_length=100)
#     admission_number = models.CharField(max_length=50, unique=True)
#     current_class = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     admission_date = models.DateField(auto_now_add=True)
#     campus = models.CharField(max_length=50, blank=True)
#     student_id = models.CharField(max_length=50, blank=True)

#     def __str__(self):
#         return self.full_name

# # --- PHASE 5: STUDENT FEE ASSIGNMENT ---
# class StudentFeeAssignment(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='fee_assignment')
#     fee_plan = models.ForeignKey(FeePlan, on_delete=models.PROTECT)
#     transport_route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, blank=True)
#     scholarship = models.ForeignKey(Scholarship, on_delete=models.SET_NULL, null=True, blank=True)

# # --- PHASE 6: STUDENT LEDGER ---
# class StudentLedger(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     description = models.CharField(max_length=255)
#     debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     reference_no = models.CharField(max_length=50, blank=True, null=True)

# # --- PHASE 7: PREVIOUS DUE SYSTEM ---
# class StudentBalance(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE)
#     outstanding_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

# # --- PHASE 8: FEE VOUCHERS ---
# class FeeVoucher(models.Model):
#     STATUS_CHOICES = [('UNPAID', 'Unpaid'), ('PARTIAL', 'Partial'), ('PAID', 'Paid'), ('OVERDUE', 'Overdue')]
#     voucher_no = models.CharField(max_length=50, unique=True)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     month = models.CharField(max_length=20)
#     issue_date = models.DateField()
#     due_date = models.DateField()
#     gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     previous_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     net_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')

# # --- PHASE 9: VOUCHER DETAILS ---
# class FeeVoucherItem(models.Model):
#     voucher = models.ForeignKey(FeeVoucher, on_delete=models.CASCADE, related_name='items')
#     fee_head = models.ForeignKey(FeeHead, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

# # --- AUTOMATION SIGNALS ---
# @receiver(post_save, sender=FeeVoucher)
# def create_ledger_entry(sender, instance, created, **kwargs):
#     if created:
#         # 1. Ledger Entry
#         StudentLedger.objects.create(
#             student=instance.student,
#             description=f"Fee Voucher Generated: {instance.voucher_no}",
#             debit=instance.net_amount,
#             balance=instance.net_amount,
#             reference_no=instance.voucher_no
#         )
        
#         # 2. Balance Update
#         balance_obj, _ = StudentBalance.objects.get_or_create(student=instance.student)
        
#         # Explicit conversion to Decimal for safety
#         current_outstanding = balance_obj.outstanding_amount or Decimal('0.00')
#         new_net_amount = Decimal(str(instance.net_amount))
        
#         balance_obj.outstanding_amount = current_outstanding + new_net_amount
#         balance_obj.save()

# # --- OTHER MODELS ---
# class Teacher(models.Model):
#     name = models.CharField(max_length=100)
#     employee_id = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)

# class Staff(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)

# class StudentPerformance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     attendance_percentage = models.FloatField()
#     average_test_score = models.FloatField()
#     risk_level = models.CharField(max_length=20)

# class Transaction(models.Model):
#     title = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=20)
#     date = models.DateField()   


# 10 email and notificatio
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

# --- PHASE 0: CUSTOM USER MODEL ---
class User(AbstractUser):
    pass

# --- PHASE 1: FEE HEADS ---
class FeeHead(models.Model):
    FREQUENCY_CHOICES = [('one_time', 'One Time'), ('monthly', 'Monthly'), ('yearly', 'Yearly')]
    name = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.frequency})"

# --- PHASE 2: FEE PLANS ---
class FeePlan(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    session = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.class_name}"

class FeePlanDetail(models.Model):
    fee_plan = models.ForeignKey(FeePlan, on_delete=models.CASCADE)
    fee_head = models.ForeignKey(FeeHead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

# --- PHASE 3: TRANSPORT ---
class TransportRoute(models.Model):
    route_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.route_name

# --- PHASE 4: SCHOLARSHIP ---
class Scholarship(models.Model):
    DISCOUNT_TYPES = [('percentage', 'Percentage'), ('fixed', 'Fixed Amount')]
    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# --- CORE MODELS ---
class Student(models.Model):
    full_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=50, unique=True)
    current_class = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    admission_date = models.DateField(auto_now_add=True)
    campus = models.CharField(max_length=50, blank=True)
    student_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.full_name

# --- PHASE 5: STUDENT FEE ASSIGNMENT ---
class StudentFeeAssignment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='fee_assignment')
    fee_plan = models.ForeignKey(FeePlan, on_delete=models.PROTECT)
    transport_route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, blank=True)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.SET_NULL, null=True, blank=True)

# --- PHASE 6: STUDENT LEDGER ---
class StudentLedger(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference_no = models.CharField(max_length=50, blank=True, null=True)

# --- PHASE 7: PREVIOUS DUE SYSTEM ---
class StudentBalance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    outstanding_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

# --- PHASE 8: FEE VOUCHERS ---
class FeeVoucher(models.Model):
    STATUS_CHOICES = [('UNPAID', 'Unpaid'), ('PARTIAL', 'Partial'), ('PAID', 'Paid'), ('OVERDUE', 'Overdue')]
    voucher_no = models.CharField(max_length=50, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    issue_date = models.DateField()
    due_date = models.DateField()
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previous_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')

# --- PHASE 9: VOUCHER DETAILS ---
class FeeVoucherItem(models.Model):
    voucher = models.ForeignKey(FeeVoucher, on_delete=models.CASCADE, related_name='items')
    fee_head = models.ForeignKey(FeeHead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

# --- NEW MODELS FOR AUTOMATION & NOTIFICATIONS ---
class FeeGenerationSettings(models.Model):
    auto_enabled = models.BooleanField(default=False)
    generation_day = models.PositiveIntegerField(default=1)
    generation_time = models.TimeField(default="09:00:00")
    send_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Auto Generation: {'Enabled' if self.auto_enabled else 'Disabled'}"

class NotificationQueue(models.Model):
    STATUS_CHOICES = (('PENDING', 'Pending'), ('SENT', 'Sent'), ('FAILED', 'Failed'))
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=(('SMS', 'SMS'), ('EMAIL', 'Email')))
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

# --- AUTOMATION SIGNALS ---
@receiver(post_save, sender=FeeVoucher)
def create_ledger_entry(sender, instance, created, **kwargs):
    if created:
        # 1. Ledger Entry
        StudentLedger.objects.create(
            student=instance.student,
            description=f"Fee Voucher Generated: {instance.voucher_no}",
            debit=instance.net_amount,
            balance=instance.net_amount,
            reference_no=instance.voucher_no
        )
        
        # 2. Balance Update
        balance_obj, _ = StudentBalance.objects.get_or_create(student=instance.student)
        
        # Explicit conversion to Decimal for safety
        current_outstanding = balance_obj.outstanding_amount or Decimal('0.00')
        new_net_amount = Decimal(str(instance.net_amount))
        
        balance_obj.outstanding_amount = current_outstanding + new_net_amount
        balance_obj.save()

# --- OTHER MODELS ---
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class StudentPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_percentage = models.FloatField()
    average_test_score = models.FloatField()
    risk_level = models.CharField(max_length=20)

class Transaction(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20)
    date = models.DateField()