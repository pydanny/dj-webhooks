import json
import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from redis import StrictRedis

from djwebhooks.decorators import redislog_hook
from djwebhooks.models import WebhookTarget
from djwebhooks.senders.redislog import make_key
from djwebhooks.utils import always_string

User = get_user_model()
WEBHOOK_EVENTS = getattr(settings, "WEBHOOK_EVENTS", None)

# Set up redis coonection
# TODO - Use other Django redis-package settings names
redis = StrictRedis(
    host=getattr(settings, "REDIS_HOST", 'localhost'),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 0))


class BasicTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        self.identifier1 = 'afdasfjasd3485'
        self.identifier2 = 'vrefr9jqaw9efj'

        self.key1 = make_key(WEBHOOK_EVENTS[0], self.user.username, self.identifier1)
        self.key2 = make_key(WEBHOOK_EVENTS[0], self.user.username, self.identifier2)

        self.webook_target = WebhookTarget.objects.create(
            owner=self.user,
            event=WEBHOOK_EVENTS[0],
            identifier=self.identifier1,
            target_url="http://httpbin.org/post"
        )
        self.fail_target = WebhookTarget.objects.create(
            owner=self.user,
            event=WEBHOOK_EVENTS[1],
            identifier=self.identifier2,
            target_url="http://httpbin.org/status/400"
        )

    def tearDown(self):

        redis.delete(self.key1)
        redis.delete(self.key2)

    def test_webhook(self):

        @redislog_hook(event=WEBHOOK_EVENTS[0])
        def basic(owner, identifier):
            return {"what": "me worry?"}

        results = basic(owner=self.user, identifier=self.identifier1)

        self.assertEqual(results['what'], "me worry?")

        self.assertEqual(redis.llen(self.key1), 1)

        d = redis.lindex(self.key1, 0)
        d = always_string(d)
        data = json.loads(d)

        self.assertEqual(data['success'], True)

    def test_failed_webhook(self):

        @redislog_hook(event=WEBHOOK_EVENTS[1])
        def basic(owner, identifier):
            return {"what": "me worry?"}

        results = basic(owner=self.user, identifier=self.identifier2)

        self.assertEqual(results['what'], "me worry?")

        # d = Delivery.objects.latest()

        # self.assertEqual(d.success, False)

    def test_event_dkwarg(self):

        @redislog_hook(number=123)
        def basic(owner, identifier):
            return {"what": "me worry?"}

        self.assertRaises(TypeError, basic, self.user)

    def test_owner_kwarg(self):

        @redislog_hook(event=WEBHOOK_EVENTS[0])
        def basic():
            return {"what": "me worry?"}

        self.assertRaises(TypeError, basic)

    def test_identifier_kwarg(self):

        @redislog_hook(event=WEBHOOK_EVENTS[0])
        def basic(owner='pydanny'):
            return {"what": "me worry?"}

        with self.assertRaises(TypeError):
            basic(owner='danny')

    def test_cant_find_webhook_target(self):
        # TODO
        pass

