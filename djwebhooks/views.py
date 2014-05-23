"""
This are sample views which probably will not match your use case.
"""

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import DetailView

from redis import StrictRedis

from .models import Delivery, WebhookTarget
from .senders.redislog import make_key

# Set up redis coonection
# TODO - Use other Django redis-package settings names
redis = StrictRedis(
    host=getattr(settings, "REDIS_HOST", 'localhost'),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 0))


class WebhookTargetDetailView(DetailView):

    max_deliveries_listed = 20

    @property
    def webhoot_target(self):
        return self.object

    @cached_property
    def object(self):
        return self.get_object()

    def get_object(self):
        if 'pk' in self.kwargs:
            return get_object_or_404(
                WebhookTarget,
                pk=self.kwargs['pk']
            )
        if 'identifier' in self.kwargs:
            return get_object_or_404(
                WebhookTarget,
                pk=self.kwargs['identifier']
            )
        raise Http404

    @cached_property
    def deliveries(self):
        return Delivery.objects.filter(
            webhoot_target=self.webhook_target
        )[:self.max_deliveries_listed]


class ProtectedWebhookTargetDetailView(WebhookTargetDetailView):

    def get_object(self):
        if 'pk' in self.kwargs:
            return get_object_or_404(
                WebhookTarget,
                pk=self.kwargs['pk'],
                owner=self.request.user

            )
        if 'identifier' in self.kwargs:
            return get_object_or_404(
                WebhookTarget,
                pk=self.kwargs['identifier'],
                owner=self.request.user
            )
        raise Http404


class WebhookTargetRedisDetailView(WebhookTargetDetailView):

    @cached_property
    def deliveries(self):
        """ Get delivery log from Redis"""
        key = make_key(
            event=self.object.event,
            owner_name=self.object.owner.username,
            identifier=self.object.identifier
        )
        return redis.lrange(key, 0, 20)


class ProtectedWebhookTargetRedisDetailView(WebhookTargetRedisDetailView):

    def get_object(self):
        if 'pk' in self.kwargs:
            return get_object_or_404(
                WebhookTarget,
                pk=self.kwargs['pk'],
                owner=self.request.user

            )
        if 'identifier' in self.kwargs:
            return get_object_or_404(
                WebhookTarget,
                pk=self.kwargs['identifier'],
                owner=self.request.user
            )
        raise Http404
