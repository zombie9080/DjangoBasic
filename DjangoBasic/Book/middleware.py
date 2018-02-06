# -*- coding: utf-8 -*-
_Author_ = 'G.Liu'

from django.utils.deprecation import MiddlewareMixin


# Customized middleware must inherit from the MiddlewareMixin class, the base class of all middleware
class CookieSetMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response.set_cookie('foo', 'bar')
        return response
