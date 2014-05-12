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

from .conf import WEBHOOKS_SENDER_CALLABLE
from ..decorators import base_hook
from ..hashes import basic_hash_function


# This is decorator that does all the lifting.
# sender_callable is set via settings.py
hook = partial(
    base_hook,
    sender_callable=WEBHOOKS_SENDER_CALLABLE,
    hash_function=basic_hash_function
)

# alias the hook function
webhook = hook
