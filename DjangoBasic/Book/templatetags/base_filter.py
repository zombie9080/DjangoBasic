# -*- coding: utf-8 -*-
_Author_ = 'G.Liu'
from django.template.library import Library

register = Library()


@register.filter
def page_filter(current_index, index):
    pass
