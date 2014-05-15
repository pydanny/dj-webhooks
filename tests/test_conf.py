from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from djwebhooks.conf import event_choices


class TestEventChoices(TestCase):

    def test_no_settings(self):
        self.assertRaises(
            ImproperlyConfigured,
            event_choices,
            None
        )

    def test_bad_settings(self):
        self.assertRaises(
            ImproperlyConfigured,
            event_choices,
            5
        )
