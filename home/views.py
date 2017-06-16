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
from models import *


def insertUser(parentId,childObj):
	obj= UserRelation.objects.get(sponserId=parentId)
	childObj.parentId=parentId
	calculate(obj.sponserId,childObj.sponserId)
	
def calculate(rootSponserId,sponserId):
	parentObj=User.objects.get(sponserId=rootSponserId)
	childObj=User.objects.get(sponserId=sponserId)
	amountAdd=0
	parentObj.amount+=(childObj.plan)*0.1
	parentObj.saveUser()
	print parentObj.amount

# tree generation

def treeGenerate(sponserId):
	
	print sponserId
	objs=UserRelation.objects.filter(parentId=sponserId)
	for obj in objs:
		usr=User.objects.get(obj.sponserId)
		print usr.username 

def home_list(request):
	return render(request, 'home/index.html', {'home':'#page-top','about':'#about','plans':'#plans','contact':'#contact','signup':'/sign_up'})

def contact_us(request):
	return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','plans':'/plans','contact':'/contact_us','signup':'/sign_up'})

def sign_up(request):
	return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','plans':'/plans','contact':'/contact_us','signup':'/sign_up'})

def about_us(request):
	return render(request, 'home/about_us.html', {})

def dashboard(request):
	parentId='1'
	childObj=UserRelation.objects.create(sponserId='3',parentId='1')
	User.objects.create(sponserId='3',username='rishabhdtu',amount=10000.00,password="asd",plan=1000)

	insertUser(parentId,childObj)
	UserRelation.objects.filter(sponserId='3').delete()
	User.objects.filter(sponserId='3').delete()

	return render(request, 'home/dashboard.html', {})

def plans(request):
	return render(request,'home/plans.html',{})

def user_profile(request):
	return render(request,'home/user_profile.html',{})

