from django.test import TestCase

from django.contrib.auth import get_user_model

from djwebhooks.decorators import webhook
from djwebhooks.models import WebhookTarget, Delivery
from djwebhooks import conf

User = get_user_model()


class BasicTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        self.webook_target = WebhookTarget.objects.create(
            owner=self.user,
            event=conf.WEBHOOK_EVENTS[0],
            target_url="http://httpbin.com"
        )

    def test_webhook(self):

        @webhook(event=conf.WEBHOOK_EVENTS[0])
        def basic(owner):
            return {"what": "me worry?"}

        results = basic(owner=self.user)

        self.assertEqual(results['what'], "me worry?")

        # TODO - figure out why two Deliveries are being made instead of one.
        #raise Exception([x.notification for x in Delivery.objects.all()])
        #raise Exception([x for x in Delivery.objects.all()])
        self.assertEqual(Delivery.objects.count(), 1)

    def tearDown(self):
        pass