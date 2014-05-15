# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from jsonfield.fields import JSONField
from model_utils.models import TimeStampedModel

from .conf import WEBHOOK_EVENTS_CHOICES

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_FORM = "application/x-www-form-urlencoded"


@python_2_unicode_compatible
class WebhookTarget(TimeStampedModel):
    """ I would prefer the name 'target', but I worry it's confusing.

        TODO - make owner/event unique_together
    """

    CONTENT_TYPE_JSON = CONTENT_TYPE_JSON
    CONTENT_TYPE_FORM = CONTENT_TYPE_FORM
    CONTENT_TYPE_CHOICES = (
        (CONTENT_TYPE_JSON, CONTENT_TYPE_JSON),
        (CONTENT_TYPE_FORM, CONTENT_TYPE_FORM)
    )

    WEBHOOK_EVENTS = WEBHOOK_EVENTS_CHOICES

    # TODO - add Webhook event choices as indivial attributes to this model, instantiated or not

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='webhooks')
    event = models.CharField(max_length=255, choices=WEBHOOK_EVENTS_CHOICES)

    target_url = models.URLField(max_length=255)

    header_content_type = models.CharField("Header content-type",
                max_length=255, choices=CONTENT_TYPE_CHOICES, default=CONTENT_TYPE_JSON)

    def __str__(self):
        return "{}=>{}".format(
            self.owner.username,
            self.target_url[:30]
        )

    class Meta:
        ordering = ["-modified"]
        get_latest_by = "modified"


# Possibly replace with redis or something else better for writes
@python_2_unicode_compatible
class Delivery(TimeStampedModel):

    webhook_target = models.ForeignKey(WebhookTarget)

    payload = JSONField()

    success = models.BooleanField(default=False)
    attempt = models.IntegerField("How many times has this been attempted to be delivered")
    hash_value = models.CharField(max_length=255, blank=True)

    notification = models.TextField("Passed back from the Senderable object", blank=True)

    # response info
    response_message = models.TextField("Whatever is sent back", blank=True)
    response_status = models.IntegerField("HTTP status code", blank=True, null=True)
    response_content_type = models.CharField(max_length=255, blank=True)

    # TODO - add rest of recorded header infos

    def __str__(self):
        return "{}=>{}=>{}".format(
            self.success,
            self.created,
            self.webhook_target
        )

    class Meta:
        ordering = ["-created"]
        get_latest_by = "created"
