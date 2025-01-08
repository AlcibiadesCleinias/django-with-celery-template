from enum import Enum


class CeleryQueue(Enum):
    """In order to use in celery server settings and when defining task queues manually."""
    DEFAULT = 'default'
    HIGH_PRIORITY = 'high_priority'
    LOW_PRIORITY = 'low_priority'
