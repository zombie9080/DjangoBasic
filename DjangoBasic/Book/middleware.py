# -*- coding: utf-8 -*-
_Author_ = 'G.Liu'

from django.utils.deprecation import MiddlewareMixin

# Customized middleware must inherit from the MiddlewareMixin class, the base class of all middleware
class CookieSetMiddleware(MiddlewareMixin):
    # A function that would be automatically called when a request is being responsed
    def process_response(self, request, response):
        response.set_cookie('foo', 'bar')
        return response
