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

# from django.db import transaction
# from django.utils import timezone
# from .models import Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, FeePlanDetail, StudentBalance, NotificationQueue
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

# class NotificationService:
#     @staticmethod
#     def queue_notifications(voucher):
#         """
#         Voucher generate hote hi SMS/Email notification ko queue mein dalta hai.
#         """
#         content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Please pay by {voucher.due_date}."
        
#         # SMS Queue
#         NotificationQueue.objects.create(
#             student=voucher.student,
#             notification_type='SMS',
#             content=content,
#             status='PENDING'
#         )

# class FeeGenerationService:
    
#     @staticmethod
#     def generate_monthly_fees(month_name):
#         """
#         Active students ke liye fee voucher generate karta hai, PDF banata hai, aur notification queue karta hai.
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
            
#             # Atomic transaction
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
                
#                 # 1. PDF Generate karna
#                 PDFGeneratorService.generate_voucher_pdf(voucher)
                
#                 # 2. Notification Queue mein dalna
#                 NotificationService.queue_notifications(voucher)
                
#                 generated_count += 1
        
#         return generated_count


# fees logs

# from django.db import transaction
# from django.utils import timezone
# from .models import (
#     Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, 
#     FeePlanDetail, StudentBalance, NotificationQueue, FeeGenerationLog
# )
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
#         folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
        
#         file_name = f"voucher_{voucher.voucher_no}.pdf"
#         file_path = os.path.join(folder_path, file_name)

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

# class NotificationService:
#     @staticmethod
#     def queue_notifications(voucher):
#         """
#         Voucher generate hote hi SMS/Email notification ko queue mein dalta hai.
#         """
#         content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Please pay by {voucher.due_date}."
        
#         NotificationQueue.objects.create(
#             student=voucher.student,
#             notification_type='SMS',
#             content=content,
#             status='PENDING'
#         )

# class FeeGenerationService:
    
#     @staticmethod
#     def generate_monthly_fees(month_name, year):
#         """
#         Active students ke liye fee voucher generate karta hai, log maintain karta hai.
#         """
#         # Log record create karein
#         log = FeeGenerationLog.objects.create(month=month_name, year=year, status='Running')
        
#         active_students = Student.objects.filter(is_active=True)
#         log.students_processed = active_students.count()
#         success_count = 0
#         failed_count = 0

#         for student in active_students:
#             try:
#                 # Duplicate Prevention
#                 if FeeVoucher.objects.filter(student=student, month=month_name).exists():
#                     continue

#                 assignment = StudentFeeAssignment.objects.filter(student=student).first()
#                 if not assignment:
#                     continue

#                 # Calculate Amounts
#                 plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
#                 gross = sum(item.amount for item in plan_items)
                
#                 balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
#                 prev_due = balance_obj.outstanding_amount
#                 net = gross + prev_due
                
#                 # Atomic transaction
#                 with transaction.atomic():
#                     voucher = FeeVoucher.objects.create(
#                         voucher_no=f"V-{student.admission_number}-{month_name}",
#                         student=student,
#                         month=month_name,
#                         issue_date=timezone.now().date(),
#                         due_date=timezone.now().date(),
#                         gross_amount=gross,
#                         previous_due=prev_due,
#                         net_amount=net,
#                         status='UNPAID'
#                     )

#                     for item in plan_items:
#                         FeeVoucherItem.objects.create(
#                             voucher=voucher,
#                             fee_head=item.fee_head,
#                             amount=item.amount
#                         )
                    
#                     # PDF & Notification
#                     PDFGeneratorService.generate_voucher_pdf(voucher)
#                     NotificationService.queue_notifications(voucher)
                    
#                     success_count += 1
            
#             except Exception as e:
#                 print(f"Error generating for {student.full_name}: {e}")
#                 failed_count += 1
        
#         # Log update karein
#         log.success_count = success_count
#         log.failed_count = failed_count
#         log.status = 'Completed'
#         log.completed_at = timezone.now()
#         log.save()
        
#         return success_count


# from django.db import transaction
# from django.utils import timezone
# from .models import (
#     Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, 
#     FeePlanDetail, StudentBalance, NotificationQueue, FeeGenerationLog
# )
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
#         folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
        
#         file_name = f"voucher_{voucher.voucher_no}.pdf"
#         file_path = os.path.join(folder_path, file_name)

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

# class NotificationService:
#     @staticmethod
#     def queue_notifications(voucher):
#         """
#         Voucher generate hote hi SMS/Email notification ko queue mein dalta hai.
#         """
#         content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Please pay by {voucher.due_date}."
        
#         NotificationQueue.objects.create(
#             student=voucher.student,
#             notification_type='SMS',
#             content=content,
#             status='PENDING'
#         )

# class FeeGenerationService:
    
#     @staticmethod
#     def generate_monthly_fees(month_name, year):
#         """
#         Active students ke liye fee voucher generate karta hai, log maintain karta hai.
#         """
#         # Log record create karein
#         log = FeeGenerationLog.objects.create(month=month_name, year=year, status='Running')
        
#         active_students = Student.objects.filter(is_active=True)
#         log.students_processed = active_students.count()
#         success_count = 0
#         failed_count = 0

#         for student in active_students:
#             try:
#                 # Duplicate Prevention
#                 if FeeVoucher.objects.filter(student=student, month=f"{month_name}-{year}").exists():
#                     continue

#                 assignment = StudentFeeAssignment.objects.filter(student=student).first()
#                 if not assignment:
#                     continue

#                 # Calculate Amounts
#                 plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
#                 gross = sum(item.amount for item in plan_items)
                
#                 balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
#                 prev_due = balance_obj.outstanding_amount
#                 net = gross + prev_due
                
#                 # Atomic transaction
#                 with transaction.atomic():
#                     voucher = FeeVoucher.objects.create(
#                         voucher_no=f"V-{student.admission_number}-{month_name}-{year}",
#                         student=student,
#                         month=f"{month_name}-{year}",
#                         issue_date=timezone.now().date(),
#                         due_date=timezone.now().date(),
#                         gross_amount=gross,
#                         previous_due=prev_due,
#                         net_amount=net,
#                         status='UNPAID'
#                     )

#                     for item in plan_items:
#                         FeeVoucherItem.objects.create(
#                             voucher=voucher,
#                             fee_head=item.fee_head,
#                             amount=item.amount
#                         )
                    
#                     # PDF & Notification
#                     PDFGeneratorService.generate_voucher_pdf(voucher)
#                     NotificationService.queue_notifications(voucher)
                    
#                     success_count += 1
            
#             except Exception as e:
#                 print(f"Error generating for {student.full_name}: {e}")
#                 failed_count += 1
        
#         # Log update karein
#         log.success_count = success_count
#         log.failed_count = failed_count
#         log.status = 'Completed'
#         log.completed_at = timezone.now()
#         log.save()
        
#         return success_count

# from django.db import transaction
# from django.utils import timezone
# from .models import (
#     Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, 
#     FeePlanDetail, StudentBalance, NotificationQueue, FeeGenerationLog,
#     AutomationJob, AutomationJobDetail
# )
# from decimal import Decimal
# from reportlab.pdfgen import canvas
# from django.conf import settings
# import os

# class PDFGeneratorService:
#     @staticmethod
#     def generate_voucher_pdf(voucher):
#         folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
        
#         file_name = f"voucher_{voucher.voucher_no}.pdf"
#         file_path = os.path.join(folder_path, file_name)

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

# class NotificationService:
#     @staticmethod
#     def queue_notifications(voucher):
#         content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Please pay by {voucher.due_date}."
        
#         NotificationQueue.objects.create(
#             student=voucher.student,
#             notification_type='SMS',
#             content=content,
#             status='PENDING'
#         )

# class FeeGenerationService:
#     @staticmethod
#     def generate_monthly_fees(month_name, year, job_id=None):
#         """
#         Active students ke liye fee voucher generate karta hai aur AutomationJob ko track karta hai.
#         """
#         # Log record create/update
#         log = FeeGenerationLog.objects.create(month=month_name, year=year, status='Running')
        
#         # Agar job_id provide ki gayi hai to job status update karein
#         job = AutomationJob.objects.get(id=job_id) if job_id else None
#         if job:
#             job.status = 'RUNNING'
#             job.save()

#         active_students = Student.objects.filter(is_active=True)
#         success_count = 0
#         failed_count = 0

#         for student in active_students:
#             try:
#                 # Duplicate Prevention
#                 if FeeVoucher.objects.filter(student=student, month=f"{month_name}-{year}").exists():
#                     continue

#                 assignment = StudentFeeAssignment.objects.filter(student=student).first()
#                 if not assignment:
#                     raise Exception("No Fee Assignment found")

#                 plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
#                 gross = sum(item.amount for item in plan_items)
                
#                 balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
#                 prev_due = balance_obj.outstanding_amount
#                 net = gross + prev_due
                
#                 with transaction.atomic():
#                     voucher = FeeVoucher.objects.create(
#                         voucher_no=f"V-{student.admission_number}-{month_name}-{year}",
#                         student=student,
#                         month=f"{month_name}-{year}",
#                         issue_date=timezone.now().date(),
#                         due_date=timezone.now().date(),
#                         gross_amount=gross,
#                         previous_due=prev_due,
#                         net_amount=net,
#                         status='UNPAID'
#                     )

#                     for item in plan_items:
#                         FeeVoucherItem.objects.create(voucher=voucher, fee_head=item.fee_head, amount=item.amount)
                    
#                     PDFGeneratorService.generate_voucher_pdf(voucher)
#                     NotificationService.queue_notifications(voucher)
                    
#                     success_count += 1
#                     if job:
#                         AutomationJobDetail.objects.create(job=job, student=student, status='SUCCESS')

#             except Exception as e:
#                 failed_count += 1
#                 if job:
#                     AutomationJobDetail.objects.create(job=job, student=student, status='FAILED', error_message=str(e))
#                 print(f"Error generating for {student.full_name}: {e}")
        
#         # Final Updates
#         log.success_count = success_count
#         log.failed_count = failed_count
#         log.status = 'Completed'
#         log.completed_at = timezone.now()
#         log.save()
        
#         if job:
#             job.status = 'COMPLETED'
#             job.success_count = success_count
#             job.failed_count = failed_count
#             job.processed_count = success_count + failed_count
#             job.completed_at = timezone.now()
#             job.save()
        
#         return success_count

# retry 

# from django.db import transaction
# from django.utils import timezone
# from .models import (
#     Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, 
#     FeePlanDetail, StudentBalance, NotificationQueue, FeeGenerationLog,
#     AutomationJob, AutomationJobDetail
# )
# from decimal import Decimal
# from reportlab.pdfgen import canvas
# from django.conf import settings
# import os

# class PDFGeneratorService:
#     @staticmethod
#     def generate_voucher_pdf(voucher):
#         folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
        
#         file_name = f"voucher_{voucher.voucher_no}.pdf"
#         file_path = os.path.join(folder_path, file_name)

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

# class NotificationService:
#     @staticmethod
#     def queue_notifications(voucher):
#         content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Please pay by {voucher.due_date}."
        
#         NotificationQueue.objects.create(
#             student=voucher.student,
#             notification_type='SMS',
#             content=content,
#             status='PENDING'
#         )

# class FeeGenerationService:
#     @staticmethod
#     def generate_monthly_fees(month_name, year, job_id=None):
#         """
#         Active students ke liye fee voucher generate karta hai aur AutomationJob ko track karta hai.
#         """
#         log = FeeGenerationLog.objects.create(month=month_name, year=year, status='Running')
        
#         job = AutomationJob.objects.get(id=job_id) if job_id else None
#         if job:
#             job.status = 'RUNNING'
#             job.save()

#         active_students = Student.objects.filter(is_active=True)
#         success_count = 0
#         failed_count = 0

#         for student in active_students:
#             try:
#                 # Duplicate Prevention
#                 if FeeVoucher.objects.filter(student=student, month=f"{month_name}-{year}").exists():
#                     continue

#                 assignment = StudentFeeAssignment.objects.filter(student=student).first()
#                 if not assignment:
#                     raise Exception("No Fee Assignment found")

#                 plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
#                 gross = sum(item.amount for item in plan_items)
                
#                 balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
#                 prev_due = balance_obj.outstanding_amount
#                 net = gross + prev_due
                
#                 with transaction.atomic():
#                     voucher = FeeVoucher.objects.create(
#                         voucher_no=f"V-{student.admission_number}-{month_name}-{year}",
#                         student=student,
#                         month=f"{month_name}-{year}",
#                         issue_date=timezone.now().date(),
#                         due_date=timezone.now().date(),
#                         gross_amount=gross,
#                         previous_due=prev_due,
#                         net_amount=net,
#                         status='UNPAID'
#                     )

#                    # services.py mein is tarah modify karein:
#                     for item in plan_items:
#                         FeeVoucherItem.objects.create(voucher=voucher, fee_head=item.fee_head, amount=item.amount)
                    
#                     print(f"--- Attempting PDF generation for: {voucher.voucher_no} ---") # YE ADD KAREIN
#                     pdf_path = PDFGeneratorService.generate_voucher_pdf(voucher)
#                     print(f"DEBUG: PDF generated at this path: {pdf_path}")
#                     print(f"--- PDF Generated at: {pdf_path} ---") # YE ADD KAREIN
                    
#                     NotificationService.queue_notifications(voucher)
                    
#                     success_count += 1
#                     if job:
#                         AutomationJobDetail.objects.create(job=job, student=student, status='SUCCESS')

#             except Exception as e:
#                 failed_count += 1
#                 if job:
#                     AutomationJobDetail.objects.create(job=job, student=student, status='FAILED', error_message=str(e))
#                 print(f"Error generating for {student.full_name}: {e}")
        
#         log.success_count = success_count
#         log.failed_count = failed_count
#         log.status = 'Completed'
#         log.completed_at = timezone.now()
#         log.save()
        
#         if job:
#             job.status = 'COMPLETED'
#             job.success_count = success_count
#             job.failed_count = failed_count
#             job.processed_count = success_count + failed_count
#             job.completed_at = timezone.now()
#             job.save()
        
#         return success_count

#     @staticmethod
#     def retry_failed_records(job_id, month_name, year):
#         """
#         Sirf failed records ko retry karne ke liye function.
#         """
#         failed_details = AutomationJobDetail.objects.filter(job_id=job_id, status='FAILED')
#         job = AutomationJob.objects.get(id=job_id)
        
#         for detail in failed_details:
#             try:
#                 # Phir se generate karne ki koshish karein
#                 # Hum wahi logic use kar rahe hain, bas student specific
#                 student = detail.student
                
#                 # Duplicate check
#                 if FeeVoucher.objects.filter(student=student, month=f"{month_name}-{year}").exists():
#                     raise Exception("Voucher already exists")

#                 assignment = StudentFeeAssignment.objects.filter(student=student).first()
#                 if not assignment:
#                     raise Exception("No Fee Assignment found")

#                 plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
#                 gross = sum(item.amount for item in plan_items)
                
#                 balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
#                 prev_due = balance_obj.outstanding_amount
#                 net = gross + prev_due
                
#                 with transaction.atomic():
#                     voucher = FeeVoucher.objects.create(
#                         voucher_no=f"V-{student.admission_number}-{month_name}-{year}",
#                         student=student,
#                         month=f"{month_name}-{year}",
#                         issue_date=timezone.now().date(),
#                         due_date=timezone.now().date(),
#                         gross_amount=gross,
#                         previous_due=prev_due,
#                         net_amount=net,
#                         status='UNPAID'
#                     )

#                     for item in plan_items:
#                         FeeVoucherItem.objects.create(voucher=voucher, fee_head=item.fee_head, amount=item.amount)
                    
#                     PDFGeneratorService.generate_voucher_pdf(voucher)
#                     NotificationService.queue_notifications(voucher)
                    
#                     # Success hone par status update
#                     detail.status = 'SUCCESS'
#                     detail.error_message = None
#                     detail.save()
                    
#                     # Job stats update
#                     job.success_count += 1
#                     job.failed_count -= 1
#                     job.save()

#             except Exception as e:
#                 detail.error_message = f"Retry Failed: {str(e)}"
#                 detail.save()
#                 print(f"Retry error for {detail.student.full_name}: {e}")

                
#pdf automation 
#  
from django.db import transaction
from django.utils import timezone
from .models import (
    Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, 
    FeePlanDetail, StudentBalance, NotificationQueue, FeeGenerationLog,
    AutomationJob, AutomationJobDetail
)
from decimal import Decimal
from reportlab.pdfgen import canvas
from django.conf import settings
import os

class PDFGeneratorService:
    @staticmethod
    def generate_voucher_pdf(voucher):
        # Folder structure creation
        folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        file_name = f"voucher_{voucher.voucher_no}.pdf"
        file_path = os.path.join(folder_path, file_name)

        # PDF Generation Logic
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
        content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Please pay by {voucher.due_date}."
        
        NotificationQueue.objects.create(
            student=voucher.student,
            notification_type='SMS',
            content=content,
            status='PENDING'
        )

class FeeGenerationService:
    @staticmethod
    def generate_monthly_fees(month_name, year, job_id=None):
        print(f"--- Fee Generation Started for {month_name}-{year} ---")
        log = FeeGenerationLog.objects.create(month=month_name, year=year, status='Running')
        
        job = AutomationJob.objects.get(id=job_id) if job_id else None
        if job:
            job.status = 'RUNNING'
            job.save()

        active_students = Student.objects.filter(is_active=True)
        success_count = 0
        failed_count = 0

        for student in active_students:
            try:
                if FeeVoucher.objects.filter(student=student, month=f"{month_name}-{year}").exists():
                    continue

                assignment = StudentFeeAssignment.objects.filter(student=student).first()
                if not assignment:
                    raise Exception("No Fee Assignment found")

                plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
                gross = sum(item.amount for item in plan_items)
                
                balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
                prev_due = balance_obj.outstanding_amount
                net = gross + prev_due
                
                with transaction.atomic():
                    voucher = FeeVoucher.objects.create(
                        voucher_no=f"V-{student.admission_number}-{month_name}-{year}",
                        student=student,
                        month=f"{month_name}-{year}",
                        issue_date=timezone.now().date(),
                        due_date=timezone.now().date(),
                        gross_amount=gross,
                        previous_due=prev_due,
                        net_amount=net,
                        status='UNPAID'
                    )

                    for item in plan_items:
                        FeeVoucherItem.objects.create(voucher=voucher, fee_head=item.fee_head, amount=item.amount)
                    
                    # PDF Generation with Debugging
                    print(f"--- Attempting PDF generation for: {voucher.voucher_no} ---")
                    pdf_path = PDFGeneratorService.generate_voucher_pdf(voucher)
                    print(f"DEBUG: PDF generated at: {pdf_path}")
                    
                    NotificationService.queue_notifications(voucher)
                    
                    success_count += 1
                    if job:
                        AutomationJobDetail.objects.create(job=job, student=student, status='SUCCESS')

            except Exception as e:
                failed_count += 1
                if job:
                    AutomationJobDetail.objects.create(job=job, student=student, status='FAILED', error_message=str(e))
                print(f"Error generating for {student.full_name}: {e}")
        
        log.status = 'Completed'
        log.success_count = success_count
        log.failed_count = failed_count
        log.completed_at = timezone.now()
        log.save()
        
        if job:
            job.status = 'COMPLETED'
            job.save()
        
        print(f"--- Fee Generation Finished. Success: {success_count}, Failed: {failed_count} ---")
        return success_count