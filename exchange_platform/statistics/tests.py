# -*- coding: utf-8 -*-
import json
from mock import Mock
from testfixtures import Replacer
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.http import HttpResponse

from ..models import SparePart


def init_db():
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
        SparePart.objects.create(name="Rudder".format(i),
                                 model='Bar',
                                 contacts='bar@bar.ru')
    for i in range(10):
        SparePart.objects.create(name="Motor".format(i),
                                 model='FooBar',
                                 price=100,
                                 contacts='foo@foo.ru')


class ViewsTest(TestCase):
    def setUp(self):
        init_db()
        setup_test_environment()

    def tearDown(self):
        SparePart.objects.all().delete()

    def test_get_web(self):
        client = Client()
        with Replacer() as r:
            mock_response = Mock(return_value=HttpResponse(status=200))
            r.replace('exchange_platform.statistics.views.ListView.render_to_response', mock_response)

            client.get('/model-stats/')
            context = mock_response.call_args[0][0]
            self.assertEqual(context.get('count'), 2)
            self.assertListEqual(context.get('results'),
                                 [dict(model='FooBar', details_count=10),
                                  dict(model="Bar", details_count=7)])

            SparePart.objects.all().delete()
            client.get('/model-stats/')
            context = mock_response.call_args[0][0]
            self.assertEqual(context.get('count'), 0)
            self.assertListEqual(context.get('results'), [])

    def test_get_api(self):
        client = Client()
        response = client.get('/api/model-stats/')
        self.assertEqual(response.json().get('count'), 2)
        self.assertListEqual(response.json().get('results'),
                             [dict(model='FooBar', details_count=10),
                              dict(model="Bar", details_count=7)])

        SparePart.objects.all().delete()
        response = client.get('/api/model-stats/')
        self.assertEqual(response.json().get('count'), 0)
        self.assertListEqual(response.json().get('results'), [])
