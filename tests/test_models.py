#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-webhooks
------------

Tests for `dj-webhooks` models module.
"""

import unittest

from django.contrib.auth import get_user_model

from djwebhooks.models import WebhookTarget, Delivery
from djwebhooks import conf

User = get_user_model()


class TestWebhookTarget(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

    def test_webhook_target(self):
        WebhookTarget.objects.create(
            owner=self.user,
            event=conf.WEBHOOK_EVENTS[0],
            target_url="http://httpbin.com"
        )
        self.assertEqual(WebhookTarget.objects.count(), 1)

    def tearDown(self):
        pass