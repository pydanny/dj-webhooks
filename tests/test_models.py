#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-webhooks
------------

Tests for `dj-webhooks` models module.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from djwebhooks.models import WebhookTarget, Delivery, event_choices

User = get_user_model()
WEBHOOK_EVENTS = getattr(settings, "WEBHOOK_EVENTS", None)


class TestWebhookTarget(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

    def test_webhook_target(self):
        webhook = WebhookTarget.objects.create(
            owner=self.user,
            event=WEBHOOK_EVENTS[0],
            target_url="http://httpbin.com"
        )
        self.assertEqual(WebhookTarget.objects.count(), 1)
        self.assertEqual(str(webhook), "testuser=>http://httpbin.com")


class TestWebhookTarget(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

    def test_delivery(self):
        webhook_target = WebhookTarget.objects.create(
            owner=self.user,
            event=WEBHOOK_EVENTS[0],
            target_url="http://httpbin.com"
        )
        delivery = Delivery.objects.create(
            webhook_target=webhook_target,
            attempt=1,
            payload={},
        )
        self.assertTrue(str(delivery).startswith('False=>'))
        self.assertTrue(str(delivery).endswith("test.success:http://httpbin.com:"))


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
