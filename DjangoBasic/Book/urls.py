# -*- coding: utf-8 -*-
_Author_ = 'G.Liu'

from django.conf.urls import url, include
from django.contrib import admin
from Book.views import login, verification, results, query_ajax, captcha, captcha_gen, \
    recognization, upload_image, storage, area_display

# Here the route mapping information for views in book is given
# which could help django to specify urls for each view
app_name = 'Book'
urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^login/verification/$', verification, name='verification'),
    url(r'^results$', results, name='results'),
    url(r'^query/$', query_ajax, name='query_ajax'),
    url(r'^captcha/$', captcha, name='captcha'),
    url(r'^captcha_gen/$', captcha_gen, name='captcha_gen'),
    url(r'^recog/$', recognization, name='recognization'),
    url(r'^upload/$', upload_image, name='upload_image'),
    url(r'^storage/$', storage, name='storage'),
    url(r'^page(\d*)/$', area_display, name='area_display')
]
