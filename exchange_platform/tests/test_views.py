# -*- coding: utf-8 -*-
import json
from mock import Mock
from testfixtures import Replacer
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.http import HttpResponse

from ..models import SparePart


def init_test_db():
    for i in xrange(4):
        SparePart.objects.create(name="Wheel{}".format(i),
                                 model='Foo',
                                 price=200.4,
                                 contacts='foo@foo.ru')
        SparePart.objects.create(name="Rudder{}".format(i),
                                 model='Bar',
                                 contacts='bar@bar.ru')
        SparePart.objects.create(name="Motor{}".format(i),
                                 model='BarBar',
                                 contacts='bar@bar.ru')


class SparePartViewTest(TestCase):
    maxDiff = None

    def setUp(self):
        init_test_db()
        setup_test_environment()

    def tearDown(self):
        SparePart.objects.all().delete()

    def test_get(self):
        test_data = [
            # (url, count, next, previous, count_result, names)
            ('/spare-part/', 12, 'http://testserver/spare-part/?page=2', None, 5,
             None),

            ('/spare-part/?page=2', 12,
             'http://testserver/spare-part/?page=3',
             'http://testserver/spare-part/', 5,
             None),
            ('/spare-part/?page=3', 12, None,
             'http://testserver/spare-part/?page=2', 2,
             None),
            ('/spare-part/?page=4', None, None, None, 0, None),

            ('/spare-part/?name=Wheel', 4, None, None, 4,
             ['Wheel{}'.format(i) for i in xrange(4)]),
            ('/spare-part/?name=Wheel1', 1, None, None, 1,
             ['Wheel1']),
            ('/spare-part/?name=wheel1', 1, None, None, 1,
             ['Wheel1']),
            ('/spare-part/?model=Foo', 4, None, None, 4,
             ['Wheel{}'.format(i) for i in xrange(4)]),
            ('/spare-part/?model=Bar', 8,
             'http://testserver/spare-part/?model=Bar&page=2', None, 5,
             ['Rudder{}'.format(i) for i in xrange(4)] + ['Motor{}'.format(i) for i in xrange(4)]),
            ('/spare-part/?name=wheel&model=foo', 4, None, None, 4,
             ['Wheel{}'.format(i) for i in xrange(4)]),
            ('/spare-part/?name=wheel&model=bar', 0, None, None, 0,
             []),
        ]
        client = Client(CONTENT_TYPE='application/json')
        for (url, count, next_, previous_, count_page, names) in test_data:
            response = client.get(url)
            self.assertEqual(response.json().get('count'), count)
            self.assertEqual(response.json().get('next'), next_)
            self.assertEqual(response.json().get('previous'), previous_)
            self.assertEqual(len(response.json().get('results', [])), count_page)
            if response.json().get('results'):
                self.assertItemsEqual(response.json().get('results')[0].keys(),
                                      ['name', 'model', 'price', 'contacts'])
            if names is not None:
                actual_names = [d['name'] for d in response.json().get('results')]
                if count != count_page:
                    self.assertTrue(set(actual_names).issubset(set(names)))
                else:
                    self.assertItemsEqual(actual_names, names)

    def test_post(self):
        client = Client(CONTENT_TYPE='application/json')
        client.post('/spare-part/',
                    data=dict(name='Pedal', model='FooFoo', contacts='a@a.ru', price=100))
        spare_part = SparePart.objects.get(name='Pedal')
        self.assertEqual(spare_part.name, 'Pedal')
        self.assertEqual(spare_part.model, 'FooFoo')
        self.assertEqual(spare_part.contacts, 'a@a.ru')
        self.assertEqual(spare_part.price, 100)

        response = client.post('/spare-part/',
                               data=dict())
        self.assertDictEqual(response.json(), {u'name': [u"This field is required."],
                                               u'model': [u"This field is required."],
                                               u'contacts': [u"This field is required."]})
        response = client.post('/spare-part/',
                               data=dict(name='Pedal', model='FooFoo', contacts='a@a.ru', price='a'))
        self.assertDictEqual(response.json(), {u'price': [u'A valid number is required.']})


class ModelStatisticsViewTest(TestCase):
    def setUp(self):
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
        setup_test_environment()

    def tearDown(self):
        SparePart.objects.all().delete()

    def test_get(self):
        client = Client(CONTENT_TYPE='application/json')
        response = client.get('/model-stats/')
        self.assertEqual(response.json().get('count'), 2)
        self.assertListEqual(response.json().get('results'),
                             [dict(model='FooBar', details_count=10),
                              dict(model="Bar", details_count=7)])

        SparePart.objects.all().delete()
        response = client.get('/model-stats/')
        self.assertEqual(response.json().get('count'), 0)
        self.assertListEqual(response.json().get('results'), [])


class TemplateViewMixinTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def tearDown(self):
        SparePart.objects.all().delete()

    def test__render_response(self):
        with Replacer() as r:
            mock_render = Mock(return_value=HttpResponse(status=200))
            r.replace('exchange_platform.views.TemplateViewMixin.render_to_response', mock_render)

            client = Client(CONTENT_TYPE='application/json')
            client.get('/model-stats/')
            self.assertEqual(mock_render.call_count, 0)

            client = Client()
            client.get('/model-stats/')
            self.assertEqual(mock_render.call_count, 1)

            client = Client(CONTENT_TYPE='text/html')
            client.get('/model-stats/')
            self.assertEqual(mock_render.call_count, 2)

    def test_list(self):
        with Replacer() as r:
            mock_render = Mock(return_value=HttpResponse(status=200))
            r.replace('exchange_platform.views.TemplateViewMixin._render_response', mock_render)

            client = Client()
            client.get('/model-stats/')
            self.assertEqual(mock_render.call_count, 1)

    def test_create(self):
        with Replacer() as r:
            mock_render = Mock(return_value=HttpResponse(status=200))
            r.replace('exchange_platform.views.TemplateViewMixin._render_response', mock_render)

            client = Client()
            client.post('/spare-part/', data=dict(name='A', model="B", contacts='ABC'))
            self.assertEqual(mock_render.call_count, 1)

