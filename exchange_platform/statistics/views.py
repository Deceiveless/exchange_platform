# -*- coding: utf-8 -*-
from django.db import models
from django.views import generic
from django.conf import settings
from rest_framework import generics, viewsets, mixins

from .serializers import *
from ..models import SparePart
from ..common import WebPagination

__author__ = 'anna'


class APIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows statistics to be viewed.
    """
    serializer_class = StatisticsSerializer
    queryset = SparePart.objects.values('model'
                                        ).annotate(details_count=models.Count('name')
                                                   ).filter(details_count__gt=settings.MIN_STATS_COUNT
                                                            ).order_by('-details_count')


class ListView(generic.TemplateView, generics.ListAPIView):
    """
    Web endpoint that allows statistics to be viewed.
    """
    template_name = 'statistics.html'
    pagination_class = WebPagination
    serializer_class = StatisticsSerializer
    queryset = SparePart.objects.values('model'
                                        ).annotate(details_count=models.Count('name')
                                                   ).filter(details_count__gt=settings.MIN_STATS_COUNT
                                                            ).order_by('-details_count')

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        context = response.data
        return self.render_to_response(context)
