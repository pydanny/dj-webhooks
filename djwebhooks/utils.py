import importlib

from django.core.exceptions import ImproperlyConfigured
from django.utils import six


def import_attribute(path):
    assert isinstance(path, six.string_types)
    pkg, attr = path.rsplit('.', 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret


def import_callable(path_or_callable):
    if not hasattr(path_or_callable, '__call__'):
        ret = import_attribute(path_or_callable)
    else:
        ret = path_or_callable
    return ret


def import_sender_callable(name):
    """ Import the stock sender for use in various places """

    try:
        return import_callable(name)
    except ImportError:
        msg = "Please set a WEBHOOKS_SENDER callable."
        raise ImproperlyConfigured(msg)
