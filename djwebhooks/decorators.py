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


from .conf import WEBHOOKS_SENDER
from .utils import import_sender_callable
from webhooks.decorators import base_hook
from webhooks.hashes import basic_hash_function

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
help(hook)

# alias the hook function
webhook = hook
