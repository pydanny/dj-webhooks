from django.core.exceptions import ImproperlyConfigured

from webhooks.senders.base import Senderable

from .conf import WEBHOOK_OWNER_FIELD, WEBHOOK_ATTEMPTS, WEBHOOKS_SENDER
from .models import WebHook, Delivery

try:
    WEBHOOKS_SENDER_CALLABLE = __import__(WEBHOOKS_SENDER)
except ImportError:
    msg = "Please set an existing WEBHOOKS_SENDER class."
    raise ImproperlyConfigured(msg)


class DjangoSenderable(Senderable):

    def notify(self, message):
            Delivery.objects.create(
            webhook=self.webhook,
            payload=self.payload,
            attempt=self.attempt,
            success=self.success,
            response_message=self.response.content,
            hash_value=self.hash_value,
            response_status=self.response.status_code
        )


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):
    """
        This is a synchronous sender callable that uses the Django ORM to store
            webhooks and the delivery log. Meant as proof of concept and not
            as something for heavy production sites.

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
        msg = "webhooks.django.senders.sender requires an 'owner' argument."
        raise TypeError(msg)
    owner = dkwargs['kwargs']

    senderobj = Senderable(
            wrapped, dkwargs, hash_value, WEBHOOK_ATTEMPTS, *args, **kwargs
    )

    # Add the webhook object just so it's around
    # TODO - error handling if this can't be found
    senderobj.webhook = WebHook.objects.get(event=event, owner=owner)

    # Get the target url and add it
    senderobj.url = senderobj.webhook.url

    # Get the payload. This overides the senderobj.payload property.
    senderobj.payload = senderobj.get_payload()

    # Get the creator and add it to the payload.
    senderobj.payload['creator'] = getattr(kwargs['creator'], WEBHOOK_OWNER_FIELD)

    # get the event and add it to the payload
    senderobj.payload['event'] = dkwargs['event']

    senderobj.send()
