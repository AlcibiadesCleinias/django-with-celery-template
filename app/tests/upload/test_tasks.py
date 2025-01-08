from unittest.mock import patch

from django.test import TestCase

from upload import tasks


class ExampleLogCounterTaskTestCase(TestCase):
    def setUp(self):
        pass

    @patch('upload.logics.redis.from_url')
    def test_successfull_call(self, mock_redis):
        # Configure the mock Redis client
        mock_redis_client = mock_redis.return_value
        mock_redis_client.incr.return_value = 1

        count = tasks.example_log_counter_task(99)

        self.assertEqual(count, 1)
        mock_redis_client.incr.assert_called_once_with('foo-counter')

    # Example of a case if example_log_counter_task call other tasks under the hood,
    #  we could check it with additional mock.
    # @patch('celery.current_app.send_task')
    # @patch('upload.logics.redis.from_url')
    # def test_successfull_call(self, mock_redis, mock_celery):
    #     # Configure the mock Redis client
    #     mock_redis_client = mock_redis.return_value
    #     mock_redis_client.incr.return_value = 1
    #
    #     count = tasks.example_log_counter_task(99)
    #
    #     # Check that additional task scheduled.
    #     self.assertTrue(mock_celery.called)