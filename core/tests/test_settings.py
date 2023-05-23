from django.conf import settings

from unittest import TestCase


class TestTimezone(TestCase):
    def test_tz_is_true(self):
        self.assertTrue(settings.USE_TZ)
