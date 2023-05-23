from decimal import Decimal
from unittest import mock
from unittest.mock import Mock

from django.test import TestCase

from concurrent_django.models.random_result import RandomResult


class TestRandomResult(TestCase):
    @mock.patch("requests.get")
    def test_custom_object_manager_creates_object_with_value_0(self, mock_response):
        mock_response.return_value = Mock(status_code=200, text="0")
        result = RandomResult.objects.create_with_random_api(0, 10)
        self.assertEqual(result.value, Decimal(0))

    @mock.patch("requests.get")
    def test_custom_object_manager_creates_object_with_value_10(self, mock_response):
        mock_response.return_value = Mock(status_code=200, text="10")
        result = RandomResult.objects.create_with_random_api(10, 100)
        self.assertEqual(result.value, Decimal(10))

    def test_custom_object_manager_raises_value_error_on_identical_min_max(self):
        with self.assertRaisesMessage(
            ValueError, "The minimum and maximum values cannot be the same"
        ):
            RandomResult.objects.create_with_random_api(0, 0)
