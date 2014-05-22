from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import DetailView

from .braces.views import LoginRequiredMixin
from .models import Delivery, WebhookTarget


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
            webhoot_target=self.webhoot_target
        )[:self.max_deliveries_listed]


class ProtectedWebhookTargetDetailView(LoginRequiredMixin, WebhookTargetDetailView):

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
        """ TODO get deliveries from Redis"""
        return []


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
