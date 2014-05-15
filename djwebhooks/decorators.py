# -*- coding: utf-8 -*-
"""
Where the hook function/decorator is stored.
Unlike the standard webhooks.decorator, this doesn't
    have the developer specify the exact sender callable.

    Write a sender function that uses the Django ORM to:

        * Queries a WebHook model to find target URLS based on event
         name and WebHook record creator
        * Logs the result in a table. Not ideal for production, but
            just as a way to track simple results
"""

from functools import partial


from django.conf import settings

from .utils import import_sender_callable
from webhooks.decorators import base_hook
from webhooks.hashes import basic_hash_function

WEBHOOKS_SENDER = getattr(settings, "WEBHOOKS_SENDER", "djwebhooks.senders.orm.sender")

# sender_callable is set via settings.WEBHOOKS_SENDER
sender_callable = import_sender_callable(WEBHOOKS_SENDER)

# This is decorator that does all the lifting.
hook = partial(
    base_hook,
    sender_callable=sender_callable,
    hash_function=basic_hash_function
)

hook.__doc__ = getattr(sender_callable, "doc", "No documentation yet!")

hook.__doc__ = "blarg"

# alias the hook function
webhook = hook


# Make the redis hook work
# This is decorator that does all the lifting.
from djwebhooks.senders.redisq import sender as sender_rq
redis_hook = partial(
    base_hook,
    sender_callable=sender_rq,
    hash_function=basic_hash_function
)