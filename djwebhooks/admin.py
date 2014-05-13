from django.contrib import admin
from django.utils import six

from .models import WebhookTarget, Delivery


class DeliveryAdmin(admin.ModelAdmin):
    """ Add this so we can see the result in Python 3.
        Currently django-jsonfield hasn't been completely ported.
    """
    if six.PY3:
        exclude = ('payload', )

admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(WebhookTarget)
