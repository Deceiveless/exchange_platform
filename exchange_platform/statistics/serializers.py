# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import SparePart

__author__ = 'anna'

__all__ = ['StatisticsSerializer']


class StatisticsSerializer(serializers.ModelSerializer):
    details_count = serializers.IntegerField()

    class Meta:
        model = SparePart
        fields = ('model', 'details_count')
