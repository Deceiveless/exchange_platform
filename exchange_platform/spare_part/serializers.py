# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import SparePart

__author__ = 'anna'

__all__ = ['SparePartSerializer']


class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePart
        fields = ('name', 'model', 'price', 'contacts')