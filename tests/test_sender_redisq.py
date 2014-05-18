import logging
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings


from djwebhooks.decorators import redis_hook
from djwebhooks.models import WebhookTarget

User = get_user_model()
WEBHOOK_EVENTS = getattr(settings, "WEBHOOK_EVENTS", None)

logger = logging.getLogger()


@override_settings(WEBHOOKS_SENDER='djwebhooks.senders.redisq.sender')
class BasicTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        self.identifier1 = 'afdasfjasd3485'
        self.identifier2 = 'vrefr9jqaw9efj'

        self.webook_target = WebhookTarget.objects.create(
            owner=self.user,
            event=WEBHOOK_EVENTS[0],
            identifier=self.identifier1,
            target_url="http://httpbin.org"
        )
        self.fail_target = WebhookTarget.objects.create(
            owner=self.user,
            event=WEBHOOK_EVENTS[1],
            identifier=self.identifier2,
            target_url="http://httpbin.org/status/400"
        )

    @override_settings(WEBHOOKS_SENDER='djwebhooks.senders.redisq.sender')
    def test_webhook(self):

        @redis_hook(event=WEBHOOK_EVENTS[0])
        def basic(owner, identifier):
            return {"what": "me worry?"}

        job = basic(owner=self.user, identifier=self.identifier1)
        for i in range(10):
            if isinstance(job, dict):
                result = job
                break
            logger.debug(i)
            time.sleep(1)
            if job.result is not None:
                result = job.result
                break

        self.assertEqual(result['what'], "me worry?")

    def test_failed_webhook(self):

        @redis_hook(event=WEBHOOK_EVENTS[1])
        def basic(owner, identifier):
            return {"what": "me worry?"}

        results = basic(owner=self.user, identifier=self.identifier2)

        self.assertEqual(results['what'], "me worry?")

        self.assertEqual(results['status_code'], 405)

    def test_event_dkwarg(self):

        @redis_hook(number=123)
        def basic(owner, identifier):
            return {"what": "me worry?"}

        self.assertRaises(TypeError, basic, self.user)

    def test_owner_kwarg(self):

        @redis_hook(event=WEBHOOK_EVENTS[0])
        def basic():
            return {"what": "me worry?"}

        self.assertRaises(TypeError, basic)

    def test_identifier_kwarg(self):

        @redis_hook(event=WEBHOOK_EVENTS[0])
        def basic(owner='pydanny'):
            return {"what": "me worry?"}

        with self.assertRaises(TypeError):
            basic(owner='danny')

    def test_cant_find_webhook_target(self):
        # TODO
        pass