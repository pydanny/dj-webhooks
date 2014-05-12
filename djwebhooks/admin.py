from django.contrib import admin

from .models import WebHook, Delivery

admin.site.register(Delivery)
admin.site.register(WebHook)
