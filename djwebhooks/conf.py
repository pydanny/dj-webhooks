from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

WEBHOOKS_SENDER = getattr(settings, "WEBHOOKS_SENDER", "webhooks.django.senders.sender")
WEBHOOK_EVENTS = getattr(settings, "WEBHOOK_EVENTS", None)
WEBHOOK_OWNER_FIELD = getattr(settings, "WEBHOOK_OWNER_FIELD", "username")
WEBHOOK_ATTEMPTS = getattr(settings, "WEBHOOK_EVENTS", (0, 15, 30, 60))

try:
    WEBHOOKS_SENDER_CALLABLE = __import__(WEBHOOKS_SENDER)
except ImportError:
    msg = "Please set an existing WEBHOOKS_SENDER class."
    raise ImproperlyConfigured(msg)
