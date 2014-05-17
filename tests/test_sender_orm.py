from django.conf import settings
from django.test import TestCase

from django.contrib.auth import get_user_model

from djwebhooks.decorators import webhook
from djwebhooks.models import WebhookTarget, Delivery
from djwebhooks import conf

User = get_user_model()
WEBHOOK_EVENTS = getattr(settings, "WEBHOOK_EVENTS", None)


class BasicTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        self.webook_target = WebhookTarget.objects.create(
            owner=self.user,
            event=WEBHOOK_EVENTS[0],
            target_url="http://httpbin.com"
        )

    def test_webhook(self):

        @webhook(event=WEBHOOK_EVENTS[0])
        def basic(owner):
            return {"what": "me worry?"}

        results = basic(owner=self.user)

        self.assertEqual(results['what'], "me worry?")

        self.assertEqual(Delivery.objects.count(), 1)
