# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def home_list(request):
    return render(request, 'home/index.html', {})

# Create your views here.
