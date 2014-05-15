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

# from django.core.exceptions import ImproperlyConfigured

from webhooks.decorators import base_hook
from webhooks.hashes import basic_hash_function

# from .conf import WEBHOOKS_SENDER

# try:
#     package = __import__(WEBHOOKS_SENDER)
#     WEBHOOKS_SENDER_CALLABLE = package.sender
# except ImportError:
#     msg = "Please set an existing WEBHOOKS_SENDER class."
#     raise ImproperlyConfigured(msg)

from djwebhooks.senders.orm import sender as WEBHOOKS_SENDER_CALLABLE


# This is decorator that does all the lifting.
# sender_callable is set via settings.py
hook = partial(
    base_hook,
    sender_callable=WEBHOOKS_SENDER_CALLABLE,
    hash_function=basic_hash_function
)

# alias the hook function
webhook = hook
