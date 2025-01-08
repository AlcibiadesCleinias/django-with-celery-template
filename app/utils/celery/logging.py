from celery.app.log import TaskFormatter


class CeleryTaskFormatter(TaskFormatter):
    """
    Providing access to Celery-specific context variables like task_id that regular formatters can't access.
    Also, providing robust workable solution for additional customisation of logs of Celery tasks.
    """
    def __init__(self, *args, datefmt=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.datefmt = datefmt
