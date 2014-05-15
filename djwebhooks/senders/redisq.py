# -*- coding: utf-8 -*-import logging
import logging

from django_rq import job

from webhooks.senders.base import Senderable
from ..conf import WEBHOOK_ATTEMPTS, WEBHOOK_OWNER_FIELD
from ..models import WebhookTarget

logger = logging.getLogger(__name__)


class DjangoRQSenderable(Senderable):

    def notify(self, message):
        logger.info(message)


@job
def worker(wrapped, dkwargs, hash_value=None, *args, **kwargs):
    """
        This is an asynchronous sender callable that uses the Django ORM to store
            webhooks. Redis is used to handle the message queue.

        dkwargs argument requires the following key/values:

            :event: A string representing an event.

        kwargs argument requires the following key/values

            :owner: The user who created/owns the event
    """

    if "event" not in dkwargs:
        msg = "webhooks.django.decorators.hook requires an 'event' argument."
        raise TypeError(msg)
    event = dkwargs['event']

    if "owner" not in kwargs:
        msg = "webhooks.django.senders.orm.sender requires an 'owner' argument."
        raise TypeError(msg)
    owner = kwargs['owner']

    senderobj = DjangoRQSenderable(
            wrapped, dkwargs, hash_value, WEBHOOK_ATTEMPTS, *args, **kwargs
    )

    # Add the webhook object just so it's around
    # TODO - error handling if this can't be found
    senderobj.webhook_target = WebhookTarget.objects.get(event=event, owner=owner)

    # Get the target url and add it
    senderobj.url = senderobj.webhook_target.target_url

    # Get the payload. This overides the senderobj.payload property.
    senderobj.payload = senderobj.get_payload()

    # Get the creator and add it to the payload.
    senderobj.payload['owner'] = getattr(kwargs['owner'], WEBHOOK_OWNER_FIELD)

    # get the event and add it to the payload
    senderobj.payload['event'] = dkwargs['event']

    return senderobj.send()


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):
    logger.debug("Starting async")
    job = worker(wrapped, dkwargs, hash_value, *args, **kwargs)
    logger.debug("Ending async")
    return job
