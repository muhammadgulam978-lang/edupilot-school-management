# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     # Yeh lines add karein error fix karne ke liye:
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to.',
#         related_name="edupilot_user_set", # Naya name
#         related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="edupilot_user_permissions_set", # Naya name
#         related_query_name="user",
#     )



# New changes from django.contrib.auth.models import AbstractUser, Group, Permission


# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     # Custom related_name to avoid clashes with default Django User model
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to.',
#         related_name="edupilot_user_set",
#         related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="edupilot_user_permissions_set",
#         related_query_name="user",
#     )

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     enrollment_number = models.CharField(max_length=50, unique=True)
#     fee_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

# class Transaction(models.Model):
#     TRANSACTION_TYPES = [('income', 'Income'), ('expense', 'Expense')]
#     title = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.amount} ({self.type})"


# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#         ('parent', 'Parent'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         related_name="edupilot_user_set",
#         related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         related_name="edupilot_user_permissions_set",
#         related_query_name="user",
#     )

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     enrollment_number = models.CharField(max_length=50, unique=True)
#     fee_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

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

# with teacher

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group, verbose_name='groups', blank=True,
        related_name="edupilot_user_set", related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='user permissions', blank=True,
        related_name="edupilot_user_permissions_set", related_query_name="user",
    )

class Student(models.Model):
    name = models.CharField(max_length=100)
    enrollment_number = models.CharField(max_length=50, unique=True)
    fee_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [('income', 'Income'), ('expense', 'Expense')]
    CATEGORY_CHOICES = [('fee', 'Fee'), ('salary', 'Salary'), ('other', 'Other')]
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.type})"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name