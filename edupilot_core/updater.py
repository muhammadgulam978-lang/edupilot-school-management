# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from .services import FeeGenerationService
# from .models import FeeGenerationSettings, AutomationJob

# # Function ko bahar nikal diya taake yeh "pickleable" ho
# def run_scheduled_job():
#     settings_obj = FeeGenerationSettings.objects.first()
#     if settings_obj and settings_obj.auto_enabled:
#         now = datetime.now()
#         # Job create karein
#         job = AutomationJob.objects.create(job_type='AUTO_GENERATION', status='PENDING')
#         FeeGenerationService.generate_monthly_fees(now.strftime("%B"), now.year, job_id=job.id)

# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")

#     # Yahan hum textual reference use kar rahe hain
#     scheduler.add_job(
#         run_scheduled_job, 
#         'interval', 
#         minutes=1, 
#         id="monthly_fee_job", 
#         replace_existing=True
#     )
    
    
#     scheduler.start()

# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from .services import FeeGenerationService
# from .models import FeeGenerationSettings, AutomationJob

# def run_scheduled_job():
#     # Job run hote waqt settings check karein
#     settings_obj = FeeGenerationSettings.objects.first()
#     if settings_obj and settings_obj.auto_enabled:
#         now = datetime.now()
#         job = AutomationJob.objects.create(job_type='AUTO_GENERATION', status='PENDING')
#         FeeGenerationService.generate_monthly_fees(now.strftime("%B"), now.year, job_id=job.id)

# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")

#     # Settings fetch karein
#     settings_obj = FeeGenerationSettings.objects.first()
    
#     if settings_obj:
#         # Cron trigger: Mahine ki 1st date, set kiye gaye time par
#         scheduler.add_job(
#             run_scheduled_job, 
#             'cron', 
#             day=settings_obj.generation_day,
#             hour=settings_obj.generation_time.hour,
#             minute=settings_obj.generation_time.minute,
#             id="monthly_fee_job", 
#             replace_existing=True
#         )
    
#     scheduler.start()


# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from .services import FeeGenerationService
# from .models import FeeGenerationSettings, AutomationJob

# def run_scheduled_job():
#     # Job run hote waqt settings check karein
#     settings_obj = FeeGenerationSettings.objects.first()
#     if settings_obj and settings_obj.auto_enabled:
#         now = datetime.now()
#         # Naya automation job create karein
#         job = AutomationJob.objects.create(job_type='AUTO_GENERATION', status='PENDING')
#         # Service call karein
#         FeeGenerationService.generate_monthly_fees(now.strftime("%B"), now.year, job_id=job.id)

# def start():
#     scheduler = BackgroundScheduler()
#     # Purane saare jobs aur execution records ko clear karne ke liye
#     scheduler.remove_all_jobs() 
#     scheduler.add_jobstore(DjangoJobStore(), "default")

#     # Settings fetch karein
#     settings_obj = FeeGenerationSettings.objects.first()
    
#     if settings_obj:
#         # Cron trigger: Set kiye gaye din aur time par
#         scheduler.add_job(
#             run_scheduled_job, 
#             'cron', 
#             day=settings_obj.generation_day,
#             hour=settings_obj.generation_time.hour,
#             minute=settings_obj.generation_time.minute,
#             id="monthly_fee_job", 
#             replace_existing=True
#         )
    
#     scheduler.start()


from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler # IMPORT ADDED
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from .services import FeeGenerationService
from .models import FeeGenerationSettings, AutomationJob

def run_scheduled_job():
    settings_obj = FeeGenerationSettings.objects.first()
    if settings_obj and settings_obj.auto_enabled:
        now = timezone.now()
        job = AutomationJob.objects.create(job_type='AUTO_GENERATION', status='PENDING')
        FeeGenerationService.generate_monthly_fees(now.strftime("%B"), now.year, job_id=job.id)

def check_and_run_job():
    settings_obj = FeeGenerationSettings.objects.first()
    if settings_obj and settings_obj.auto_enabled:
        now = timezone.now()
        # Admin set time check
        if now.day == settings_obj.generation_day and \
           now.hour == settings_obj.generation_time.hour and \
           now.minute == settings_obj.generation_time.minute:
            run_scheduled_job()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Har 1 minute baad check karega
    scheduler.add_job(
        check_and_run_job, 
        'interval', 
        minutes=1, 
        id="check_fee_generation_job", 
        replace_existing=True
    )
    scheduler.start()