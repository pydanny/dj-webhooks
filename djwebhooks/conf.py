from django.conf import settings

WEBHOOKS_SENDER = getattr(settings, "WEBHOOKS_SENDER", "djwebhooks.senders")
WEBHOOK_EVENTS = getattr(settings, "WEBHOOK_EVENTS", None)
WEBHOOK_OWNER_FIELD = getattr(settings, "WEBHOOK_OWNER_FIELD", "username")
WEBHOOK_ATTEMPTS = getattr(settings, "WEBHOOK_EVENTS", (0, 15, 30, 60))

