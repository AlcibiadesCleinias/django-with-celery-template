from celery import shared_task
from celery.utils.log import get_task_logger

from upload import logics

# Get Celery-based logger.
logger = get_task_logger('celery.task.hello_django.upload')


@shared_task
def example_log_counter_task(smth_serialisable: int) -> int:
    """
    Example call of task with logic written in separate module.
    """
    logger.info('Celery logger in tasks: start example_log_counter_task...')
    counter = logics.example_log_counter(smth_serialisable)
    logger.info('Celery logger in tasks: result of logic method call: %s', counter)
    return counter