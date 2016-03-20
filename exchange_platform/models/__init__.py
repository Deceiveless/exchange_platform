# -*- coding: utf-8 -*-

from django.db import models

__author__ = 'anna'


class SparePart(models.Model):
    id = models.AutoField(primary_key=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(db_index=True, max_length=200, null=False)
    model = models.CharField(db_index=True, max_length=200, null=False)
    price = models.FloatField(null=True)
    contacts = models.TextField(null=False, blank=False)