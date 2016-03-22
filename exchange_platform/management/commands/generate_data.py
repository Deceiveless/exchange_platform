# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from exchange_platform.models import SparePart

__author__ = 'anna'


class Command(BaseCommand):
    help = "Generate initialdata"

    def handle(self, *args, **options):
        SparePart.objects.all().delete()
        for i in xrange(4):
            SparePart.objects.create(name="Wheel{}".format(i),
                                     model='Foo',
                                     price=200.4,
                                     contacts='foo@foo.ru')
        for i in xrange(5):
            SparePart.objects.create(name="Wheel{}".format(i),
                                     model='FooFoo',
                                     price=200.4,
                                     contacts='foo@foo.ru')

        for i in xrange(7):
            SparePart.objects.create(name="Rudder{}".format(i),
                                     model='Bar',
                                     contacts='bar@bar.ru')
        for i in range(10):
            SparePart.objects.create(name="Motor{}".format(i),
                                     model='FooBar',
                                     price=100,
                                     contacts='foo@foo.ru')
