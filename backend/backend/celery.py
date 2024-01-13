import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    broker_url='pyamqp://guest:guest@localhost//',
    result_backend='rpc://',
)
app.conf.beat_schedule = {
    'enrollment_start_date': {
        'task': 'enrollments.tasks.enrollment_start_date',
        'schedule': crontab(minute='*/5'),
    },
    'application_deadline': {
        'task': 'enrollments.tasks.application_deadline',
        'schedule': crontab(minute='*/5'),
    },
    'decision_deadline': {
        'task': 'enrollments.tasks.decision_deadline',
        'schedule': crontab(minute='*/5'),
    },
}

app.autodiscover_tasks()
