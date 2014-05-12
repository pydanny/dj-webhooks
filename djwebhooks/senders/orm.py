import json
from time import sleep

import requests

from .conf import WEBHOOK_OWNER_FIELD, WEBHOOK_ATTEMPTS
from ..encoders import WebHooksJSONEncoder
from .models import WebHook, Delivery


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

    # TODO - error handling if this can't be found
    webhook = WebHook.objects.get(event=event, owner=owner)

    # Create the payload by calling the hooked/wrapped function.
    payload = wrapped(*args, **kwargs)

    # Add the hash value if there is one.
    if hash_value is not None and len(hash_value) > 0:
        payload['hash'] = hash_value

    # Get the creator and add it to the payload.
    creator = getattr(kwargs['creator'], WEBHOOK_OWNER_FIELD)
    payload['creator'] = creator

    # get the event and add it to the payload
    event = dkwargs['event']
    payload['event'] = event

    # Dump the payload to json
    data = json.dumps(payload, cls=WebHooksJSONEncoder)

    # Loop through the attempts and log each attempt
    for i, attempt in enumerate(range(len(WEBHOOK_ATTEMPTS) - 1)):
        # log each attempt.
        # print(
        #     "Attempt: {attempt}, {target_url}\n{payload}".format(
        #         attempt=attempt,
        #         target_url=webhook.url,
        #         payload=data
        #     )
        # )

        # post the payload
        r = requests.post(webhook.url, payload)

        # anything with a 200 status code  is a success
        if r.status_code >= 200 and r.status_code < 300:
            # Record the current status
            Delivery.objects.create(
                webhook=webhook,
                payload=data,
                attempt=i + 1,
                success=True,
                response_message=r.content,
                hash_value=hash_value,
                response_status=r.status_code
            )
            # Exit the sender function.
            return True

        # Record the current status of things and try again.
        Delivery.objects.create(
            webhook=webhook,
            payload=data,
            attempt=i + 1,
            success=True,
            response_message=r.content,
            hash_value=hash_value,
            response_status=r.status_code
        )

        # Wait a bit before the next attempt
        sleep(attempt)

    # Exit the sender function.
    return False
