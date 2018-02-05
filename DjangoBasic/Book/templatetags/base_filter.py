# -*- coding: utf-8 -*-
_Author_ = 'G.Liu'
from django.template.library import Library

register = Library()


@register.filter
def page_filter(page_index, current_index):
    if abs(current_index - page_index) <= 2:
        return True
    return False
