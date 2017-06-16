# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import models
from models import *
import random
import string

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)


from .forms import ContactForm
from django.shortcuts import render

from models import *
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

def insertUser(parentId,childId):
	# obj= UserRelation.objects.get(sponserId=parentId)
	# childObj.parentId=parentId
	calculate(parentId,childId)
	
def calculate(rootSponserId,sponserId):
	parentObj=User.objects.get(sponserId=rootSponserId)
	childObj=User.objects.get(sponserId=sponserId)
	amountAdd=0
	parentObj.amount+=(childObj.plan)*0.1
	parentObj.saveUser()
	print parentObj.amount

# tree generation

def treeGenerate(sponserId):
	
	# print sponserId

	objs=UserRelation.objects.filter(parentId=sponserId)
	# print type(objs)
	# usr=User.objects.get(objs[0].sponserId)
	# print usr.username
	return objs
	# for obj in objs:
	# 	sid=obj.sponserId
	# 	print sid
	    # usr=User.objects.get(obj.sponserId)
	#     print usr.username
	# return render(request, 'home/dashboard.html', {'objs':objs})


def home_list(request):
	return render(request, 'home/index.html', {'home':'#page-top','about':'#about','products':'#products','contact':'#contact','signup':'/sign_up'})

def contact_us(request):
	return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'})

def sign_up(request):
	if request.method == "POST":
		sponserId="".join(random.choice(string.ascii_uppercase+string.digits) for x in range (0,6))
		username=request.POST.get('userName')
		password=password,=request.POST.get('password')
		confirmPassword=request.POST.get('confirmPassword')
		product = int(request.POST.get('product'))
		# print username

		User.objects.create(sponserId=sponserId,username=username,password=password, plan=product,amount=0.00)


		firstName= request.POST.get('firstName')
		lastName=request.POST.get('lastName')
		phoneNo=request.POST.get('mobNumber')
		email= request.POST.get('email')
		address= request.POST.get('address')
		UserDetails.objects.create(username=username,firstName=firstName,lastName=lastName, phoneNo=phoneNo,email=email,address=address)
		

		holderName=request.POST.get('holderName')
		IFSCCode=request.POST.get('ifscCode')
		bankName=request.POST.get('bankName')
		branchName=request.POST.get('branchName')
		a=request.POST.get('accountType')
		if(a=="Saving"):
			accountType=True
		else:
			accountType=False
		accountNo=request.POST.get('accNumber')
		panCard=request.POST.get('panCard')
		panNo=request.POST.get('panCardNumber')
		aadhaarCard = request.POST.get('aadhaarCard')
		aadhaarNo = request.POST.get('aadhaarCardNumber')

		UserAccount.objects.create(username=username,holderName=holderName,IFSCCode=IFSCCode,bankName=bankName,branchName=branchName,
			accountType=accountType,accountNo=accountNo,panCard=panCard,panNo=panNo,aadhaarCard=aadhaarCard,aadhaarNo=aadhaarNo)

		parentId=request.POST.get('sponserId')
		UserRelation.objects.create(sponserId=sponserId,parentId=parentId)
		# print firstName,username,lastName,phoneNo,email,address

		insertUser(parentId,sponserId)


		return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'})
	else:
		return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'})

def login(request):
	if request.method == "POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		print username
		# validation 

		usr=User.objects.get(username=username)
		objs=treeGenerate(usr.sponserId)
		return render(request, 'home/dashboard.html', {'objs':objs})

		# return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'}) #{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'}) 
	else:
	    return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'}) #{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'}) 

def about_us(request):
	return render(request, 'home/about_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'})

def dashboard(request):
	parentId='1'
	childObj=UserRelation.objects.create(sponserId='3',parentId='1')
	User.objects.create(sponserId='3',username='rishabhdtu',amount=10000.00,password="asd",plan=1000)

	insertUser(parentId,childObj)
	UserRelation.objects.filter(sponserId='3').delete()
	User.objects.filter(sponserId='3').delete()

	return render(request, 'home/dashboard.html', {})

def products(request):
	return render(request,'home/products.html',{})

def user_profile(request):
	return render(request,'home/user_profile.html',{})


def contact(request):
	form_class = ContactForm

	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get('contact_name', '')
			contact_email = request.POST.get('contact_email', '')
			contact_subject = request.POST.get('contact_subject', '')
			form_content = request.POST.get('content','')


			template = get_template('home/contact_template.txt')
			context = {
					'contact_name': contact_name,
					'contact_email': contact_email,
					'contact_subject': contact_subject,
					'form_content' : form_content,
				}
			content = template.render(context)

			email = EmailMessage(
				"New contact form submission",
				content,
				"Your website" + '',
				['ddproductions.2017@gmail.com'],
				headers = {'Reply-To': contact_email }
				)
			email.send()
			return redirect('contact')
	return render(request,'home/contact.html', {'form': form_class,})






