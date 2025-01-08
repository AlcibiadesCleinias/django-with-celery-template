from os import environ

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from kombu import Exchange, Queue

from utils.celery.queues import CeleryQueue

environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_django.settings')

_CELERY_DEFAULT_RESULT_EXPIRES = 300

# To configure Celery logging from convenient Django settings module.
@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)


app = Celery('hello_django')
# Allow of standardised control of settings to be loaded from Django settings module (as expected).
# While the standard setup is supported it is recommended to use current module to seup all Celery related staff.
# The 'CELERY_' namespace prefix is required for all celery-related
# configuration keys in Django settings according to Celery docs.
app.config_from_object('django.conf:settings', namespace='CELERY')

conf = app.conf
conf.timezone = 'UTC'
# Default queue settings.
# Example usage:
# # Content of .../tasks.py
# @app.task(queue='high_priority')
# def high_priority_task():
#     return "This task goes to high priority queue"
#
# @app.task(queue='default')
# def default_priority_task():
#     return "This task goes to default priority queue"
#
# # Using queue on task execution
# high_priority_task.apply_async(args=[], queue='high_priority')
# default_priority_task.apply_async(args=[], queue='default')
# low_priority_task.apply_async(args=[], queue='low_priority')
_high_priority_queue = CeleryQueue.HIGH_PRIORITY.value
_default_priority_queue = CeleryQueue.DEFAULT.value
_low_priority_queue = CeleryQueue.LOW_PRIORITY.value
conf.task_queues = (
    Queue(_high_priority_queue, Exchange(_high_priority_queue), routing_key=_high_priority_queue),
    Queue(_default_priority_queue, Exchange(_default_priority_queue), routing_key=_default_priority_queue),
    Queue(_low_priority_queue, Exchange(_low_priority_queue), routing_key=_low_priority_queue),
)
conf.task_default_queue = _default_priority_queue
conf.task_default_exchange = _default_priority_queue
conf.task_default_routing_key = _default_priority_queue
conf.beat_schedule = {
    # Human-readable description of the task.
    'each_minute_example_log_counter_task': {
        'task': 'upload.tasks.example_log_counter_task',
        'schedule': crontab(),  # instead of string cron definition use crontab fabric.
        'args': (99,),
    },
    # E.g. of additional Celery cleanup task - in case of aggressive usage of celery cluster for big amount of small
    # tasks (by default Celery configure each 24 hours cleanup).
    'backend_cleanup': {
        'task': 'celery.backend_cleanup',
        'schedule': int(environ.get('CELERY_RESULT_EXPIRES', _CELERY_DEFAULT_RESULT_EXPIRES)),
    },
}
# In case of agressive usage of Celery it is better to disable limit
#  (https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-pool-limit).
conf.broker_pool_limit = int(environ.get('CELERY_BROKER_POOL_LIMIT', 0))
conf.broker_url = environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
conf.result_backend = environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
conf.result_expires = int(environ.get('CELERY_RESULT_EXPIRES', _CELERY_DEFAULT_RESULT_EXPIRES))

# Enable autodiscover of tasks in all installed Django apps (tasks.py).
app.autodiscover_tasks()
