# -*- coding: utf-8 -*-
from rest_framework import pagination, response

__author__ = 'anna'


class WebPagination(pagination.PageNumberPagination):
    template = "pagination.html"

    def get_paginated_response(self, data):
        context = self.get_html_context()
        return response.Response({
            'pagination': context,
            'count': self.page.paginator.count,
            'results': data
        })