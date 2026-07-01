
# from django.db import transaction
# from django.utils import timezone
# from .models import (
#     Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, 
#     FeePlanDetail, StudentBalance, NotificationQueue, FeeGenerationLog,
#     AutomationJob, AutomationJobDetail, Teacher, SalaryVoucher, SalaryStructure,
#     SalaryAutomationJob, SalaryAutomationJobDetail
# )
# from decimal import Decimal
# from reportlab.pdfgen import canvas
# from django.conf import settings
# import os
# from datetime import datetime

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

# class SalaryPDFGeneratorService:
#     @staticmethod
#     def generate_salary_pdf(voucher):
#         try:
#             folder_path = os.path.join(settings.MEDIA_ROOT, 'salary_vouchers')
#             if not os.path.exists(folder_path):
#                 os.makedirs(folder_path)
            
#             file_name = f"salary_{voucher.teacher.teacher_id}_{voucher.month}_{voucher.year}.pdf"
#             file_path = os.path.join(folder_path, file_name)

#             print(f"DEBUG: Trying to save Salary PDF at: {file_path}") 

#             c = canvas.Canvas(file_path)
#             c.setFont("Helvetica-Bold", 16)
#             c.drawString(100, 800, "TEACHER SALARY VOUCHER")
            
#             c.setFont("Helvetica", 12)
#             c.drawString(100, 770, f"Teacher: {voucher.teacher.name}")
#             c.drawString(100, 750, f"Month: {voucher.month} - {voucher.year}")
#             c.drawString(100, 730, f"Net Salary: {voucher.net_salary}")
            
#             c.save()
#             print(f"DEBUG: Salary PDF saved successfully!")
#             return file_path
#         except Exception as e:
#             print(f"CRITICAL ERROR: Failed to generate Salary PDF: {e}")
#             return None

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

# class NotificationDispatcherService:
#     @staticmethod
#     def send_pending_notifications():
#         pending_list = NotificationQueue.objects.filter(status='PENDING')
#         for notif in pending_list:
#             try:
#                 print(f"--- Sending SMS to {notif.student}: {notif.content} ---")
#                 notif.status = 'SENT'
#                 notif.save()
#             except Exception as e:
#                 notif.status = 'FAILED'
#                 notif.save()
#                 print(f"Error sending SMS: {e}")

# class FeeGenerationService:
#     @staticmethod
#     def generate_monthly_fees(month_name, year, job_id=None):
#         print(f"--- Fee Generation Started for {month_name}-{year} ---")
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
                    
#                     pdf_path = PDFGeneratorService.generate_voucher_pdf(voucher)
#                     NotificationService.queue_notifications(voucher)
                    
#                     success_count += 1
#                     if job:
#                         AutomationJobDetail.objects.create(job=job, student=student, status='SUCCESS')

#             except Exception as e:
#                 failed_count += 1
#                 if job:
#                     AutomationJobDetail.objects.create(job=job, student=student, status='FAILED', error_message=str(e))
#                 print(f"Error generating for {student.full_name}: {e}")
        
#         log.status = 'Completed'
#         log.success_count = success_count
#         log.failed_count = failed_count
#         log.completed_at = timezone.now()
#         log.save()
        
#         if job:
#             job.status = 'COMPLETED'
#             job.save()
        
#         return success_count

# class SalaryAutomationService:
#     @staticmethod
#     def generate_salaries():
#         month = datetime.now().strftime("%B")
#         year = datetime.now().year

#         # Duplicate Protection
#         if SalaryVoucher.objects.filter(month=month, year=year).exists():
#             print("Salary already generated for this month.")
#             return

#         job = SalaryAutomationJob.objects.create(status='RUNNING')
#         teachers = Teacher.objects.filter(is_active=True)
        
#         for teacher in teachers:
#             try:
#                 earnings = (teacher.basic_salary or 0) + (teacher.house_allowance or 0) + \
#                            (teacher.medical_allowance or 0) + (teacher.transport_allowance or 0) + \
#                            (teacher.utility_allowance or 0) + (teacher.special_allowance or 0) + \
#                            (teacher.overtime or 0)
                
#                 deductions = SalaryStructure.objects.filter(teacher=teacher).values_list('deductions', flat=True).first() or 0
#                 net_salary = earnings - deductions

#                 voucher = SalaryVoucher.objects.create(
#                     teacher=teacher,
#                     month=month,
#                     year=year,
#                     net_salary=net_salary,
#                     status='UNPAID'
#                 )

#                 SalaryPDFGeneratorService.generate_salary_pdf(voucher)
#                 job.success_count += 1
#             except Exception as e:
#                 job.failed_count += 1
#                 SalaryAutomationJobDetail.objects.create(job=job, teacher=teacher, status='FAILED', error_message=str(e))
        
#         job.status = 'COMPLETED'
#         job.completed_at = timezone.now()
#         job.save()

#         # services.py ke end mein ye add karein
# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime

# def start_salary_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(run_salary_automation, 'interval', minutes=1)
#     scheduler.start()

# def run_salary_automation():
#     from .models import SalaryAutomationSettings
#     settings = SalaryAutomationSettings.objects.first()
#     if settings and settings.auto_enabled:
#         now = datetime.now()
#         # Time aur Day match check
#         if now.day == settings.generation_day and \
#            now.hour == settings.generation_time.hour and \
#            now.minute == settings.generation_time.minute:
#             SalaryAutomationService.generate_salaries()
from django.db import transaction
from django.utils import timezone
from .models import (
    Student, StudentFeeAssignment, FeeVoucher, FeeVoucherItem, 
    FeePlanDetail, StudentBalance, NotificationQueue, FeeGenerationLog,
    AutomationJob, AutomationJobDetail, Teacher, SalaryVoucher, SalaryStructure,
    SalaryAutomationJob, SalaryAutomationJobDetail
)
from reportlab.pdfgen import canvas
from django.conf import settings
import os
from datetime import datetime, timedelta
from decimal import Decimal

class PDFGeneratorService:
    @staticmethod
    def generate_voucher_pdf(voucher):
        folder_path = os.path.join(settings.MEDIA_ROOT, 'vouchers')
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        file_path = os.path.join(folder_path, f"voucher_{voucher.voucher_no}.pdf")
        c = canvas.Canvas(file_path)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 800, "SCHOOL FEE VOUCHER")
        c.setFont("Helvetica", 12)
        c.drawString(100, 770, f"Voucher No: {voucher.voucher_no}")
        c.drawString(100, 750, f"Student: {voucher.student.full_name}")
        c.drawString(100, 730, f"Month: {voucher.month}")
        c.drawString(100, 710, f"Issue Date: {voucher.issue_date}")
        c.drawString(100, 690, f"Due Date: {voucher.due_date}")
        c.drawString(100, 670, f"Gross Amount: {voucher.gross_amount}")
        c.drawString(100, 650, f"Discount: {voucher.discount}")
        c.drawString(100, 630, f"Previous Due: {voucher.previous_due}")
        c.drawString(100, 610, f"NET PAYABLE: {voucher.net_amount}")
        c.save()
        return file_path

class SalaryPDFGeneratorService:
    @staticmethod
    def generate_salary_pdf(voucher):
        try:
            folder_path = os.path.join(settings.MEDIA_ROOT, 'salary_vouchers')
            if not os.path.exists(folder_path): os.makedirs(folder_path)
            file_path = os.path.join(folder_path, f"salary_{voucher.teacher.teacher_id}_{voucher.month}_{voucher.year}.pdf")
            c = canvas.Canvas(file_path)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 800, "TEACHER SALARY VOUCHER")
            c.setFont("Helvetica", 12)
            c.drawString(100, 770, f"Teacher: {voucher.teacher.name}")
            c.drawString(100, 750, f"Month: {voucher.month} - {voucher.year}")
            c.drawString(100, 730, f"Net Salary: {voucher.net_salary}")
            c.save()
            return file_path
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            return None

class NotificationService:
    @staticmethod
    def queue_notifications(voucher):
        content = f"Dear Parent, Fee Voucher {voucher.voucher_no} for {voucher.month} is generated. Amount: {voucher.net_amount}. Due by {voucher.due_date}."
        NotificationQueue.objects.create(
            student=voucher.student, 
            notification_type='SMS', 
            content=content, 
            status='PENDING'
        )

class NotificationDispatcherService:
    @staticmethod
    def send_pending_notifications():
        for notif in NotificationQueue.objects.filter(status='PENDING'):
            try:
                print(f"--- Sending SMS to {notif.student}: {notif.content} ---")
                notif.status = 'SENT'
                notif.save()
            except Exception as e:
                notif.status = 'FAILED'
                notif.save()

class FeeGenerationService:
    @staticmethod
    def generate_monthly_fees(month_name, year, job_id=None):
        """
        Generate monthly fee vouchers for all active students
        """
        print(f"\n{'='*60}")
        print(f"📋 FEE GENERATION STARTED: {month_name}-{year}")
        print(f"{'='*60}\n")
        
        log = FeeGenerationLog.objects.create(month=month_name, year=year, status='Running')
        job = AutomationJob.objects.filter(id=job_id).first() if job_id else None
        
        if job: 
            job.status = 'RUNNING'
            job.save()

        success_count = 0
        failed_count = 0
        
        # Get all active students
        students = Student.objects.filter(is_active=True)
        print(f"Total Active Students: {students.count()}\n")

        for student in students:
            try:
                # ✅ CHECK 1: Prevent duplicate vouchers
                existing = FeeVoucher.objects.filter(
                    student=student, 
                    month=month_name,
                    issue_date__year=year
                ).exists()
                
                if existing:
                    print(f"⏭️  SKIP: {student.full_name} - Voucher already exists")
                    continue
                
                # ✅ CHECK 2: Get fee assignment
                assignment = StudentFeeAssignment.objects.filter(student=student).first()
                if not assignment:
                    raise Exception(f"No fee assignment found")
                
                # ✅ CHECK 3: Get fee plan items
                plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
                if not plan_items.exists():
                    raise Exception(f"No fee heads in plan")
                
                # ✅ CALCULATE: Gross Amount
                gross = sum(Decimal(str(item.amount)) for item in plan_items)
                
                # ✅ ADD: Transport fee if assigned
                if assignment.transport_route:gross += Decimal(str(assignment.transport_route.amount or 0))

                # ✅ GET: Previous outstanding
                balance_obj, _ = StudentBalance.objects.get_or_create(student=student)
                prev_due = balance_obj.outstanding_amount
                
                # ✅ CALCULATE: Discount (scholarship)
                discount = Decimal('0')
                if assignment.scholarship:
                    if assignment.scholarship.discount_type == 'percentage':
                        discount = (gross * Decimal(str(assignment.scholarship.value))) / Decimal('100')
                    else:
                        discount = Decimal(str(assignment.scholarship.value))
                
                # ✅ FINAL: Net Amount
                net_amount = gross + prev_due - discount
                
                # ✅ DATES
                now = datetime.now()
                issue_date = now.date()
                due_date = issue_date + timedelta(days=15)
                
                # ✅ CREATE VOUCHER (with ALL fields)
                with transaction.atomic():
                    voucher = FeeVoucher.objects.create(
                        voucher_no=f"V-{student.admission_number}-{month_name}-{year}",
                        student=student,
                        month=month_name,
                        issue_date=issue_date,
                        due_date=due_date,
                        gross_amount=gross,
                        discount=discount,
                        fine=Decimal('0'),
                        previous_due=prev_due,
                        net_amount=net_amount,
                        status='UNPAID'
                    )
                    
                    # Add fee line items
                    for item in plan_items:
                        FeeVoucherItem.objects.create(
                            voucher=voucher,
                            fee_head=item.fee_head,
                            amount=item.amount
                        )
                    
                    # Add transport item if applicable
                    if assignment.transport_route:
                        from .models import FeeHead
                        transport_head, _ = FeeHead.objects.get_or_create(
                            name='Transport',
                            defaults={'frequency': 'monthly', 'status': True}
                        )
                        FeeVoucherItem.objects.create(
                            voucher=voucher,
                            fee_head=transport_head,
                            amount=assignment.transport_route.amount
                        )
                    
                    # Generate PDF
                    PDFGeneratorService.generate_voucher_pdf(voucher)
                    
                    # Queue SMS/Email notification
                    NotificationService.queue_notifications(voucher)
                    
                    # Log success
                    if job:
                        AutomationJobDetail.objects.create(
                            job=job,
                            student=student,
                            status='SUCCESS'
                        )
                    
                    success_count += 1
                    print(f"✅ {student.full_name}: Rs.{net_amount} (Voucher: {voucher.voucher_no})")
                    
            except Exception as e:
                failed_count += 1
                error_msg = str(e)
                print(f"❌ {student.full_name}: {error_msg}")
                
                if job:
                    AutomationJobDetail.objects.create(
                        job=job,
                        student=student,
                        status='FAILED',
                        error_message=error_msg
                    )
        
        # ✅ FINALIZE LOG
        log.status = 'Completed'
        log.students_processed = success_count + failed_count
        log.success_count = success_count
        log.failed_count = failed_count
        log.completed_at = timezone.now()
        log.save()
        
        # ✅ FINALIZE JOB
        if job:
            job.status = 'COMPLETED'
            job.processed_count = success_count + failed_count
            job.success_count = success_count
            job.failed_count = failed_count
            job.completed_at = timezone.now()
            job.save()
        
        print(f"\n{'='*60}")
        print(f"✅ COMPLETED: {success_count} Success | ❌ {failed_count} Failed")
        print(f"{'='*60}\n")
        
        return success_count

    @staticmethod
    def retry_failed_records(job_id, month, year):
        """Retry failed voucher generations"""
        job = AutomationJob.objects.get(id=job_id)
        failed_details = AutomationJobDetail.objects.filter(job=job, status='FAILED')
        
        for detail in failed_details:
            try:
                # Retry logic
                assignment = StudentFeeAssignment.objects.filter(student=detail.student).first()
                if not assignment:
                    raise Exception("No fee assignment")
                
                plan_items = FeePlanDetail.objects.filter(fee_plan=assignment.fee_plan)
                gross = sum(Decimal(str(item.amount)) for item in plan_items)
                
                voucher = FeeVoucher.objects.create(
                    voucher_no=f"V-{detail.student.admission_number}-{month}-{year}",
                    student=detail.student,
                    month=month,
                    issue_date=datetime.now().date(),
                    due_date=datetime.now().date() + timedelta(days=15),
                    gross_amount=gross,
                    net_amount=gross,
                    status='UNPAID'
                )
                
                for item in plan_items:
                    FeeVoucherItem.objects.create(voucher=voucher, fee_head=item.fee_head, amount=item.amount)
                
                detail.status = 'SUCCESS'
                detail.error_message = None
                detail.save()
            except Exception as e:
                detail.error_message = str(e)
                detail.save()

class SalaryAutomationService:
    @staticmethod
    def generate_salaries():
        month = datetime.now().strftime("%B")
        year = datetime.now().year

        # Duplicate Protection
        if SalaryVoucher.objects.filter(month=month, year=year).exists():
            print("⏭️  Salary already generated for this month")
            return

        job = SalaryAutomationJob.objects.create(status='RUNNING')
        teachers = Teacher.objects.filter(is_active=True)
        
        for teacher in teachers:
            try:
                # Calculate total earnings
                earnings = (teacher.basic_salary or 0) + \
                          (teacher.house_allowance or 0) + \
                          (teacher.medical_allowance or 0) + \
                          (teacher.transport_allowance or 0) + \
                          (teacher.utility_allowance or 0) + \
                          (teacher.special_allowance or 0) + \
                          (teacher.overtime or 0)
                
                # Get deductions
                deductions = SalaryStructure.objects.filter(teacher=teacher).values_list('deductions', flat=True).first() or 0
                net_salary = Decimal(str(earnings)) - Decimal(str(deductions))

                # Create voucher
                voucher = SalaryVoucher.objects.create(
                    teacher=teacher,
                    month=month,
                    year=year,
                    net_salary=net_salary,
                    status='UNPAID'
                )

                SalaryPDFGeneratorService.generate_salary_pdf(voucher)
                job.success_count += 1
                print(f"✅ {teacher.name}: Rs.{net_salary}")
                
            except Exception as e:
                job.failed_count += 1
                SalaryAutomationJobDetail.objects.create(
                    job=job, 
                    teacher=teacher, 
                    status='FAILED', 
                    error_message=str(e)
                )
                print(f"❌ {teacher.name}: {str(e)}")
        
        job.status = 'COMPLETED'
        job.completed_at = timezone.now()
        job.save()
        
        print(f"✅ Salary generation: {job.success_count} success, {job.failed_count} failed")