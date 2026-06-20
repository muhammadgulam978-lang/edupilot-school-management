# from django.db import transaction
# from django.utils import timezone
# from .models import Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, FeePlanDetail, StudentBalance
# from decimal import Decimal

# class FeeGenerationService:
    
#     @staticmethod
#     def generate_monthly_fees(month_name):
#         """
#         1. Fetch Active Students
#         2. Check for Duplicates (Duplicate Prevention)
#         3. Calculate charges based on Fee Plan
#         4. Create Voucher and Items
#         """
#         active_students = Student.objects.filter(is_active=True)
#         generated_count = 0

#         for student in active_students:
#             # Duplicate Prevention: Check if voucher already exists for this month
#             if FeeVoucher.objects.filter(student=student, month=month_name).exists():
#                 continue

#             assignment = StudentFeeAssignment.objects.filter(student=student).first()
#             if not assignment:
#                 continue

#             # Calculate Gross Amount
#             plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
#             gross = sum(item.amount for item in plan_items)
            
#             # Previous Due (from StudentBalance)
#             balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
#             prev_due = balance_obj.outstanding_amount

#             # Net Calculation
#             net = gross + prev_due
            
#             # Atomic transaction to ensure data integrity
#             with transaction.atomic():
#                 voucher = FeeVoucher.objects.create(
#                     voucher_no=f"V-{student.admission_number}-{month_name}",
#                     student=student,
#                     month=month_name,
#                     issue_date=timezone.now().date(),
#                     due_date=timezone.now().date(),
#                     gross_amount=gross,
#                     previous_due=prev_due,
#                     net_amount=net,
#                     status='UNPAID'
#                 )

#                 for item in plan_items:
#                     FeeVoucherItem.objects.create(
#                         voucher=voucher,
#                         fee_head=item.fee_head,
#                         amount=item.amount
#                     )
                
#                 generated_count += 1
        

#         return generated_count


# from django.db import transaction
# from django.utils import timezone
# from .models import Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, FeePlanDetail, StudentBalance
# from decimal import Decimal
# from reportlab.pdfgen import canvas
# from django.conf import settings
# import os

# class PDFGeneratorService:
#     @staticmethod
#     def generate_voucher_pdf(voucher):
#         """
#         Voucher data ko lekar PDF generate karta hai aur media/vouchers folder mein save karta hai.
#         """
#         # 1. Folder path check aur creation
#         folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
        
#         # 2. File path define karna
#         file_name = f"voucher_{voucher.voucher_no}.pdf"
#         file_path = os.path.join(folder_path, file_name)

#         # 3. PDF creation logic
#         c = canvas.Canvas(file_path)
#         c.setFont("Helvetica-Bold", 16)
#         c.drawString(100, 800, "SCHOOL FEE VOUCHER")
        
#         c.setFont("Helvetica", 12)
#         c.drawString(100, 770, f"Voucher No: {voucher.voucher_no}")
#         c.drawString(100, 750, f"Student: {voucher.student.full_name}")
#         c.drawString(100, 730, f"Month: {voucher.month}")
#         c.drawString(100, 710, f"Gross Amount: {voucher.gross_amount}")
#         c.drawString(100, 690, f"Previous Due: {voucher.previous_due}")
#         c.drawString(100, 670, f"Net Payable: {voucher.net_amount}")
        
#         c.save()
#         return file_path

# class FeeGenerationService:
    
#     @staticmethod
#     def generate_monthly_fees(month_name):
#         """
#         Active students ke liye fee voucher generate karta hai aur PDF banata hai.
#         """
#         active_students = Student.objects.filter(is_active=True)
#         generated_count = 0

#         for student in active_students:
#             # Duplicate Prevention: Check if voucher already exists
#             if FeeVoucher.objects.filter(student=student, month=month_name).exists():
#                 continue

#             assignment = StudentFeeAssignment.objects.filter(student=student).first()
#             if not assignment:
#                 continue

#             # Calculate Amounts
#             plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
#             gross = sum(item.amount for item in plan_items)
            
#             balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
#             prev_due = balance_obj.outstanding_amount
#             net = gross + prev_due
            
#             # Atomic transaction to ensure data integrity
#             with transaction.atomic():
#                 voucher = FeeVoucher.objects.create(
#                     voucher_no=f"V-{student.admission_number}-{month_name}",
#                     student=student,
#                     month=month_name,
#                     issue_date=timezone.now().date(),
#                     due_date=timezone.now().date(),
#                     gross_amount=gross,
#                     previous_due=prev_due,
#                     net_amount=net,
#                     status='UNPAID'
#                 )

#                 for item in plan_items:
#                     FeeVoucherItem.objects.create(
#                         voucher=voucher,
#                         fee_head=item.fee_head,
#                         amount=item.amount
#                     )
                
#                 # PDF Generate karna (Voucher save hone ke baad)
#                 PDFGeneratorService.generate_voucher_pdf(voucher)
                
#                 generated_count += 1
        
#         return generated_count


# email serivece
from django.db import transaction
from django.utils import timezone
from .models import Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, FeePlanDetail, StudentBalance, NotificationQueue
from decimal import Decimal
from reportlab.pdfgen import canvas
from django.conf import settings
import os

class PDFGeneratorService:
    @staticmethod
    def generate_voucher_pdf(voucher):
        """
        Voucher data ko lekar PDF generate karta hai aur media/vouchers folder mein save karta hai.
        """
        # 1. Folder path check aur creation
        folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # 2. File path define karna
        file_name = f"voucher_{voucher.voucher_no}.pdf"
        file_path = os.path.join(folder_path, file_name)

        # 3. PDF creation logic
        c = canvas.Canvas(file_path)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 800, "SCHOOL FEE VOUCHER")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 770, f"Voucher No: {voucher.voucher_no}")
        c.drawString(100, 750, f"Student: {voucher.student.full_name}")
        c.drawString(100, 730, f"Month: {voucher.month}")
        c.drawString(100, 710, f"Gross Amount: {voucher.gross_amount}")
        c.drawString(100, 690, f"Previous Due: {voucher.previous_due}")
        c.drawString(100, 670, f"Net Payable: {voucher.net_amount}")
        
        c.save()
        return file_path

class NotificationService:
    @staticmethod
    def queue_notifications(voucher):
        """
        Voucher generate hote hi SMS/Email notification ko queue mein dalta hai.
        """
        content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Please pay by {voucher.due_date}."
        
        # SMS Queue
        NotificationQueue.objects.create(
            student=voucher.student,
            notification_type='SMS',
            content=content,
            status='PENDING'
        )

class FeeGenerationService:
    
    @staticmethod
    def generate_monthly_fees(month_name):
        """
        Active students ke liye fee voucher generate karta hai, PDF banata hai, aur notification queue karta hai.
        """
        active_students = Student.objects.filter(is_active=True)
        generated_count = 0

        for student in active_students:
            # Duplicate Prevention: Check if voucher already exists
            if FeeVoucher.objects.filter(student=student, month=month_name).exists():
                continue

            assignment = StudentFeeAssignment.objects.filter(student=student).first()
            if not assignment:
                continue

            # Calculate Amounts
            plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
            gross = sum(item.amount for item in plan_items)
            
            balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
            prev_due = balance_obj.outstanding_amount
            net = gross + prev_due
            
            # Atomic transaction
            with transaction.atomic():
                voucher = FeeVoucher.objects.create(
                    voucher_no=f"V-{student.admission_number}-{month_name}",
                    student=student,
                    month=month_name,
                    issue_date=timezone.now().date(),
                    due_date=timezone.now().date(),
                    gross_amount=gross,
                    previous_due=prev_due,
                    net_amount=net,
                    status='UNPAID'
                )

                for item in plan_items:
                    FeeVoucherItem.objects.create(
                        voucher=voucher,
                        fee_head=item.fee_head,
                        amount=item.amount
                    )
                
                # 1. PDF Generate karna
                PDFGeneratorService.generate_voucher_pdf(voucher)
                
                # 2. Notification Queue mein dalna
                NotificationService.queue_notifications(voucher)
                
                generated_count += 1
        
        return generated_count