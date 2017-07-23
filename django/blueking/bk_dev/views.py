# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import datetime



# def current_datetime(request):
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#     return HttpResponse(html)

from django.template import Context,Template
from django.template.loader import get_template,render_to_string
from django.shortcuts import render_to_response
# def current_datetime(request):
#     now = datetime.datetime.now()
#     rendered = render_to_string('current_datetime.html',{'current_date': now})
#     return HttpResponse(rendered)

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_date': now})