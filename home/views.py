# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)

#from .forms import UserLoginForm



from django.shortcuts import render

def home_list(request):
	return render(request, 'home/index.html', {'home':'#page-top','about':'#about','plans':'#plans','contact':'#contact','signup':'/sign_up'})

def contact_us(request):
    return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','plans':'/plans','contact':'/contact_us','signup':'/sign_up'})

def sign_up(request):
    return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','plans':'/plans','contact':'/contact_us','signup':'/sign_up'})

def about_us(request):
    return render(request, 'home/about_us.html', {})

def dashboard(request):
    return render(request, 'home/dashboard.html', {})

def plans(request):
	return render(request,'home/plans.html',{})

