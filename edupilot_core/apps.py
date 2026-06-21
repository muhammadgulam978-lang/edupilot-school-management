# from django.apps import AppConfig

# class EdupilotCoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'edupilot_core'

# import os
# from django.apps import AppConfig

# class EdupilotCoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'edupilot_core'

#     def ready(self):
#         # RUN_MAIN check ensures scheduler only starts once
#         if os.environ.get('RUN_MAIN'):
#             from . import updater
#             updater.start()
# apps.
import os
from django.apps import AppConfig

class EdupilotCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edupilot_core'

    def ready(self):
        # RUN_MAIN check ensures the scheduler only starts once 
        # (prevents duplicate jobs in development mode)
        if os.environ.get('RUN_MAIN') == 'true':
            from . import updater
            updater.start()