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


from webhooks.decorators import base_hook
from webhooks.hashes import basic_hash_function


from .senders import orm_callable, redislog_callable, redisq_callable


# This is decorator that does all the lifting.
hook = partial(
    base_hook,
    sender_callable=orm_callable,
    hash_function=basic_hash_function
)


# alias the hook function
webhook = hook


# Make the redis log hook work
# This is decorator that does all the lifting.
redislog_hook = partial(
    base_hook,
    sender_callable=redislog_callable,
    hash_function=basic_hash_function
)

# alias the redis_hook function
redislog_webhook = redislog_hook


# Make the redis queue hook work
# This is decorator that does all the lifting.
redisq_hook = partial(
    base_hook,
    sender_callable=redisq_callable,
    hash_function=basic_hash_function
)

# alias the redis_hook function
redisq_webhook = redisq_hook


