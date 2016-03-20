# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import SparePart

__author__ = 'anna'

__all__ = ['SparePartSerializer', 'ModelSerializer']


class SparePartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SparePart
        fields = ('name', 'model', 'price', 'contacts')


class ModelSerializer(serializers.HyperlinkedModelSerializer):
    details_count = serializers.IntegerField()

    class Meta:
        model = SparePart
        fields = ('model', 'details_count')