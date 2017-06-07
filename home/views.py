# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def home_list(request):
    return render(request, 'home/index.html', {})

def contact_us(request):
    return render(request, 'home/contact_us.html', {})

def sign_up(request):
    return render(request, 'home/sign_up.html', {})

def about_us(request):
    return render(request, 'home/about_us.html', {})

def dashboard(request):
    return render(request, 'home/dashboard.html', {})


# Create your views here.
