# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import SparePart

__author__ = 'anna'


class SparePartTest(TestCase):
    def setUp(self):
        SparePart.objects.create(name="Wheel", model='Foo', price=200.4, contacts='foo@foo.ru')
        SparePart.objects.create(name="Rudder", model='Bar', contacts='bar@bar.ru')
        SparePart.objects.create(name="Motor", model='Bar', price=100, contacts='foo@foo.ru')

    def tearDown(self):
        SparePart.objects.all().delete()

    def test_crud(self):
        spare_parts = SparePart.objects.all()
        self.assertEqual(len(spare_parts), 3)

        spare_part = SparePart.objects.get(name='Rudder')
        self.assertEqual(spare_part.name, 'Rudder')
        self.assertEqual(spare_part.price, None)
        spare_part.price = 200
        spare_part.save()
        spare_part = SparePart.objects.get(name='Rudder')
        self.assertEqual(spare_part.price, 200.0)

        SparePart.objects.all().filter(name='Rudder').delete()
        spare_parts = SparePart.objects.all()
        self.assertEqual(len(spare_parts), 2)

