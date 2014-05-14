# -*- coding: utf-8 -*-
import json
import logging
from time import sleep


import requests
from django_rq import job

from ..conf import WEBHOOK_ATTEMPTS
from ..encoders import WebHooksJSONEncoder

logger = logging.getLogger(__name__)


@job
def worker(wrapped, dkwargs, hash_value=None, *args, **kwargs):

    # Get the URL from the kwargs
    url = kwargs.get('url', None)
    if url is None:
        url = dkwargs['url']

    # Create the payload by calling the hooked/wrapped function.
    payload = wrapped(*args, **kwargs)

    # Add the hash value if there is one.
    if hash_value is not None and len(hash_value) > 0:
        payload['hash'] = hash_value

    # Dump the payload to json
    data = json.dumps(payload, cls=WebHooksJSONEncoder)

    for attempt in range(len(WEBHOOK_ATTEMPTS) - 1):
        # Print each attempt. In practice, this would write to logs
        msg = "Attempt: {attempt}, {url}\n{payload}".format(
                attempt=attempt + 1,
                url=url,
                payload=data
            )
        logger.debug(msg)

        # post the payload
        r = requests.post(url, payload)

        # anything with a 200 status code  is a success
        if r.status_code >= 200 and r.status_code < 300:
            # Exit the sender function.  Here we provide the payload as a result.
            #   In practice, this means writing the result to a datastore.
            logger.debug("Success!")
            return payload

        # Wait a bit before the next attempt
        sleep(attempt)
    else:
        logger.debug("Could not send webhook")

    # Exit the sender function.  Here we provide the payload as a result for
    #   display when this function is run outside of the sender function.
    return payload


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):

    logger.debug("Starting async")
    worker(wrapped, dkwargs, hash_value=None, *args, **kwargs)
    worker.delay
    logger.debug("Ending async")
