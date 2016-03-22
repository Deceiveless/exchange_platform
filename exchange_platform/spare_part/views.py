# -*- coding: utf-8 -*-
from django.views import generic
from django.shortcuts import redirect
from rest_framework import filters, generics, exceptions, viewsets, mixins
from rest_framework.renderers import TemplateHTMLRenderer

from .serializers import *
from .filters import SparePartFilter
from ..models import SparePart
from ..common import WebPagination

__author__ = 'anna'


class ListView(generic.TemplateView, generics.ListAPIView):
    """
    Web endpoint that allows spare parts to be viewed.
    """
    template_name = 'main.html'
    pagination_class = WebPagination
    serializer_class = SparePartSerializer
    queryset = SparePart.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SparePartFilter
    ordering = ('-dt_created', 'name',)

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        context = response.data
        context.update(query=request.query_params)
        return self.render_to_response(context)


class FormView(generic.TemplateView, generics.CreateAPIView):
    """
    Web endpoint that allows spare parts to be created.
    """
    template_name = 'create.html'
    serializer_class = SparePartSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return self.render_to_response(dict(serializer=serializer))

    def create(self, request, *args, **kwargs):
        try:
            super(FormView, self).create(request, *args, **kwargs)
        except exceptions.ValidationError, ex:
            context = {'data': request.data, 'errors': dict(ex.detail)}
            return self.render_to_response(context)
        else:
            return redirect('/spare-parts')


class APIView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows spare parts to be viewed or created.
    """
    serializer_class = SparePartSerializer
    queryset = SparePart.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SparePartFilter
    ordering = ('-dt_created', 'name',)
