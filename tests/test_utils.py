from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from djwebhooks.utils import import_sender_callable


class TestSenderCallableImportTest(TestCase):

    def test_import_sender_callable(self):
        from djwebhooks.senders.orm import sender
        self.assertEqual(import_sender_callable("djwebhooks.senders.orm.sender"), sender)

    def test_failed_import(self):
        self.assertRaises(
            ImproperlyConfigured,
            import_sender_callable,
            "no.such.sender"
        )
