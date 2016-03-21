# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import SparePart

__author__ = 'anna'

__all__ = ['SparePartSerializer', 'StatsModelSerializer']


class SparePartSerializer(serializers.ModelSerializer):
    # filter_name = serializers.CharField()
    # filter_model = serializers.CharField()

    class Meta:
        model = SparePart
        fields = ('name', 'model', 'price', 'contacts')


class StatsModelSerializer(serializers.ModelSerializer):
    details_count = serializers.IntegerField()

    class Meta:
        model = SparePart
        fields = ('model', 'details_count')