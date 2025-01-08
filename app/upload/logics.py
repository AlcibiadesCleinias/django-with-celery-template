import logging

from django.conf import settings
import redis

COUNTER_KEY = 'foo-counter'

logger = logging.getLogger(__name__)


def example_log_counter(*args, **kwargs) -> int:
    _redis = redis.from_url(settings.REDIS_URL)
    logger.info("Root logger called in example_log_counter method...")
    return _redis.incr(COUNTER_KEY)
