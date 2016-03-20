# -*- coding: utf-8 -*-
from rest_framework import filters, viewsets, mixins
from django.db import models
from django.views.generic import TemplateView

from ..models import SparePart
from .serializers import *
from .filter import SparePartFilter

__author__ = 'anna'

# todo: make templates/ tests


class TemplateViewMixin(TemplateView):
    # todo add update/destroy/retrieve or redefine __getattr__

    def _render_response(self, request, response):
        if request.META.get('CONTENT_TYPE') == 'application/json':
            return response
        # return response
        return self.render_to_response(response.data)

    def list(self, request, *args, **kwargs):
        response = super(TemplateViewMixin, self).list(request, *args, **kwargs)
        return self._render_response(request, response)

    def create(self, request, *args, **kwargs):
        response = super(TemplateViewMixin, self).create(request, *args, **kwargs)
        return self._render_response(request, response)


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class ListOrCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class SparePartView(TemplateViewMixin, ListOrCreateViewSet):
    """
    API endpoint that allows spare parts to be viewed or created.
    """
    template_name = 'create.html'
    serializer_class = SparePartSerializer
    queryset = SparePart.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SparePartFilter
    ordering = ('-dt_created', 'name',)
    # filter_fields = ('name', 'model')


class ModelStatisticsView(TemplateViewMixin, ListViewSet):
    """
    API endpoint that allows statistics to be viewed.
    """
    MIN_STATS_COUNT = 5
    template_name = 'statistics.html'
    serializer_class = ModelSerializer
    queryset = SparePart.objects.values('model'
                                        ).annotate(details_count=models.Count('name')
                                                   ).filter(details_count__gt=MIN_STATS_COUNT
                                                            ).order_by('-details_count')

