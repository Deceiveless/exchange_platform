# -*- coding: utf-8 -*-
from mock import Mock
from testfixtures import Replacer
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.http import HttpResponse

from ..models import SparePart
from .serializers import SparePartSerializer


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

    test_get_data = [
        # (url, count, next, previous, count_result, names)
        ('/spare-parts/', 12, '/spare-parts/?page=2', None, 5,
         None),

        ('/spare-parts/?page=2', 12,
         '/spare-parts/?page=3',
         '/spare-parts/', 5,
         None),
        ('/spare-parts/?page=3', 12, None,
         '/spare-parts/?page=2', 2,
         None),
        ('/spare-parts/?page=4', None, None, None, 0, None),

        ('/spare-parts/?name=Wheel', 4, None, None, 4,
         ['Wheel{}'.format(i) for i in xrange(4)]),
        ('/spare-parts/?name=Wheel1', 1, None, None, 1,
         ['Wheel1']),
        ('/spare-parts/?name=wheel1', 1, None, None, 1,
         ['Wheel1']),
        ('/spare-parts/?model=Foo', 4, None, None, 4,
         ['Wheel{}'.format(i) for i in xrange(4)]),
        ('/spare-parts/?model=Bar', 8,
         '/spare-parts/?model=Bar&page=2', None, 5,
         ['Rudder{}'.format(i) for i in xrange(4)] + ['Motor{}'.format(i) for i in xrange(4)]),
        ('/spare-parts/?name=wheel&model=foo', 4, None, None, 4,
         ['Wheel{}'.format(i) for i in xrange(4)]),
        ('/spare-parts/?name=wheel&model=bar', 0, None, None, 0,
         []),
    ]

    def setUp(self):
        init_test_db()
        setup_test_environment()

    def tearDown(self):
        SparePart.objects.all().delete()

    def get_context(self, mock_response):
        if not mock_response.call_args:
            return {}
        if not mock_response.call_args[0]:
            return {}
        return mock_response.call_args[0][0]

    def test_get_api(self):
        client = Client()
        for (url, count, next_, previous_, count_page, names) in self.test_get_data:
            response = client.get('/api{}'.format(url))
            self.assertEqual(response.json().get('count'), count)
            next_ = 'http://testserver/api{}'.format(next_) if next_ else None
            previous_ = 'http://testserver/api{}'.format(previous_) if previous_ else None
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

    def test_get_web(self):
        client = Client()
        for (url, count, next_, previous_, count_page, names) in self.test_get_data:
            with Replacer() as r:
                mock_response = Mock(return_value=HttpResponse(status=200))
                r.replace('exchange_platform.spare_part.views.ListView.render_to_response', mock_response)
                client.get(url)
                context = self.get_context(mock_response)

                self.assertEqual(context.get('count'), count)
                next_ = 'http://testserver{}'.format(next_) if next_ else None
                previous_ = 'http://testserver{}'.format(previous_) if previous_ else None
                self.assertEqual(context.get('pagination', {}).get('next_url'), next_)
                self.assertEqual(context.get('pagination', {}).get('previous_url'), previous_)
                self.assertEqual(len(context.get('results', [])), count_page)
                if context.get('results'):
                    self.assertItemsEqual(context.get('results')[0].keys(),
                                          ['name', 'model', 'price', 'contacts'])

                if names is None:
                    continue
                actual_names = [d['name'] for d in context.get('results')]
                if count != count_page:
                    self.assertTrue(set(actual_names).issubset(set(names)))
                else:
                    self.assertItemsEqual(actual_names, names)

    def test_post_api(self):
        client = Client()
        client.post('/api/spare-parts/',
                    data=dict(name='Pedal', model='FooFoo', contacts='a@a.ru', price=100))
        spare_part = SparePart.objects.get(name='Pedal')
        self.assertEqual(spare_part.name, 'Pedal')
        self.assertEqual(spare_part.model, 'FooFoo')
        self.assertEqual(spare_part.contacts, 'a@a.ru')
        self.assertEqual(spare_part.price, 100)

        response = client.post('/api/spare-parts/',
                               data=dict())
        self.assertDictEqual(response.json(), {u'name': [u"This field is required."],
                                               u'model': [u"This field is required."],
                                               u'contacts': [u"This field is required."]})
        response = client.post('/api/spare-parts/',
                               data=dict(name='Pedal', model='FooFoo', contacts='a@a.ru', price='a'))
        self.assertDictEqual(response.json(), {u'price': [u'A valid number is required.']})

    def test_post_web(self):
        client = Client()
        with Replacer() as r:
            mock_response = Mock(return_value=HttpResponse(status=200))
            r.replace('exchange_platform.spare_part.views.FormView.render_to_response', mock_response)
            r.replace('django.shortcuts.redirect', Mock())

            client.post('/spare-part/',
                        data=dict(name='Pedal', model='FooFoo', contacts='a@a.ru', price=100))
            spare_part = SparePart.objects.get(name='Pedal')
            self.assertEqual(spare_part.name, 'Pedal')
            self.assertEqual(spare_part.model, 'FooFoo')
            self.assertEqual(spare_part.contacts, 'a@a.ru')
            self.assertEqual(spare_part.price, 100)

            client.post('/spare-part/',
                        data=dict())
            context = self.get_context(mock_response)
            self.assertDictEqual(context.get('errors', {}), {u'name': [u"This field is required."],
                                           u'model': [u"This field is required."],
                                           u'contacts': [u"This field is required."]})
            mock_response.reset_mock()
            client.post('/spare-part/',
                        data=dict(name='Pedal', model='FooFoo', contacts='a@a.ru', price='a'))
            context = self.get_context(mock_response)
            self.assertDictEqual(context.get('errors', {}), {u'price': [u'A valid number is required.']})

    def test_get_form_web(self):
        client = Client()
        with Replacer() as r:
            mock_response = Mock(return_value=HttpResponse(status=200))
            r.replace('exchange_platform.spare_part.views.FormView.render_to_response', mock_response)
            client.get('/spare-part/')

            context = self.get_context(mock_response)
            self.assertIsInstance(context['serializer'], SparePartSerializer)


