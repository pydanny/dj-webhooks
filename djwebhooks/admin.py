from django.contrib import admin

from .models import WebhookTarget, Delivery

admin.site.register(Delivery)
admin.site.register(WebhookTarget)
