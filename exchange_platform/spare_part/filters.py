# -*- coding: utf-8 -*-
import django_filters
from rest_framework import filters

from ..models import SparePart

__author__ = 'anna'

__all__ = ['SparePartFilter']


class SparePartFilter(filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type='icontains')
    model = django_filters.CharFilter(name="model", lookup_type='icontains')

    class Meta:
        model = SparePart
        fields = ['name', 'model']
