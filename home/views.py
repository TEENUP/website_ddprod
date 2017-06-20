# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from . import models
from models import *
import random
import string
import hashlib
import hmac


from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)


from .forms import ContactForm
from django.shortcuts import render
# from django.template import RequestContext

from models import *
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
import re

regexForSponserId="^[A-Z0-9]*$"
SECRET="qwerty"

def make_salt():
    return "".join(random.choice(string.letters) for x in range (0,5))

def make_pw_hash(name,pw,salt=None):
    if not salt:
        salt=make_salt()
    h=hashlib.sha256(name+pw+salt).hexdigest()
    return "%s,%s"%(h,salt)

def hash_str(s):
	return hmac.new(str(SECRET),str(s)).hexdigest()

def make_secure_val(s):
	print "SPONSER ID "+s
	return "%s|%s"%(s,hash_str(s))

def check_secure_val(h):
    check_value=h.split('|')
    if hash_str(check_value[0])==check_value[1]:
        return check_value[0]
    return None

def valid_pw(name,pw,h):
    salt=h.split(',')[1]
    return h==make_pw_hash(name,pw,salt)


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

def isLoggedIn(request):
	user_id=""
	if 'user_id' in request.COOKIES:
		user_id= request.COOKIES['user_id']
	if user_id:
		sponserId=check_secure_val(user_id)
		if sponserId:
			return True
	return False

def home_list(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/index.html', {'home':'#page-top','about':'#about','products':'#products','contact':'#contact','greet':greet,'logout':logout})
	else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return render(request, 'home/index.html', {'home':'#page-top','about':'#about','products':'#products','contact':'#contact','greet':greet})


def contact_us(request):
	return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'})

def validateSponserId(sponserId):
	if len(sponserId)!=6:
		return False
	isValid = not not re.match(regexForSponserId,sponserId)
	if not isValid:
		return False
	else:
		user=User.objects.filter(sponserId=sponserId)
		if user.count()>0:
			return True
		else:
			return False
	return False

def validateUsername(username):
	user=User.objects.filter(username=username)
	if user.count()>0:
		return False
	return True

def validatePassword(password,confirmPassword):
	if password == confirmPassword:
		return True
	return False

def sign_up(request):
	if request.method == "POST":
		parentId=request.POST.get('sponserId')
		isSponserIdValid=validateSponserId(parentId)
		errorSponserId=""
		if not isSponserIdValid:
			errorSponserId="Invalid Sponser Id"

		sponserId="".join(random.choice(string.ascii_uppercase+string.digits) for x in range (0,6))
		
		username=request.POST.get('userName')
		isUsernameValid = validateUsername(username)
		errorUsername=""
		if(not isUsernameValid):
			errorUsername="User Already Exists"

		password=request.POST.get('password')
		confirmPassword=request.POST.get('confirmPassword')

		isPasswordValid = validatePassword(password,confirmPassword)
		errorPassword=""
		if(not isPasswordValid):
			errorPassword="Passwords didn't match"

		product = int(request.POST.get('product'))
		firstName= request.POST.get('firstName')
		lastName=request.POST.get('lastName')
		phoneNo=request.POST.get('mobNumber')
		email= request.POST.get('email')
		address= request.POST.get('address')
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
		
		#validation
		if isSponserIdValid and isUsernameValid and isPasswordValid:
			h_password=make_pw_hash(username,password)
			User.objects.create(sponserId=sponserId,username=username,password=h_password, plan=product,amount=0.00)
			UserDetails.objects.create(username=username,firstName=firstName,lastName=lastName, phoneNo=phoneNo,email=email,address=address)
			UserAccount.objects.create(username=username,holderName=holderName,IFSCCode=IFSCCode,bankName=bankName,branchName=branchName,
				accountType=accountType,accountNo=accountNo,panCard=panCard,panNo=panNo,aadhaarCard=aadhaarCard,aadhaarNo=aadhaarNo)
			UserRelation.objects.create(sponserId=sponserId,parentId=parentId)
			# Payment
			insertUser(parentId,sponserId)
			#set Cookie
			# redirect to homepage
			id_to_send=make_secure_val(str(sponserId))
			# print "ID TO SEND"+id_to_send
			# print "SPONSERID"+sponserId
			response = redirect('/')
			response.set_cookie('user_id', id_to_send)
			return response
		else:
			# Render The page with errors
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up','errorSponserId':errorSponserId,'errorUsername':errorUsername,'errorPassword':errorPassword})
	else:
		if isLoggedIn(request):
			return redirect('/')
		else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet})


def login(request):
	if request.method == "POST":
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=User.objects.filter(username=username)
		errorLogin="Incorrect Username OR Password"
		if user.count()>0:
			usr=User.objects.get(username=username)
			h_value=usr.password
			if valid_pw(username,password,h_value):
				user_id=usr.sponserId
				id_to_send=make_secure_val(str(user_id))
				response = redirect('/dashboard')
				response.set_cookie('user_id', id_to_send)
				return response
			else:

				# Incorrect Password But Write Incorrect Username OR password
				return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up','name':username,'password':password,'errorLogin':errorLogin})
		else:
			# Incorrect Username but Write Incorrect Username OR password
				return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up','name':username,'password':password,'errorLogin':errorLogin})

		

		# return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'}) #{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'}) 
	else:
		if isLoggedIn(request):
			return redirect('/')
		else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet})

def about_us(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/about_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout})
	else:
		greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		return render(request, 'home/about_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet})


def dashboard(request):
	# parentId='1'
	# childObj=UserRelation.objects.create(sponserId='3',parentId='1')
	# User.objects.create(sponserId='3',username='rishabhdtu',amount=10000.00,password="asd",plan=1000)

	# insertUser(parentId,childObj)
	# UserRelation.objects.filter(sponserId='3').delete()
	# User.objects.filter(sponserId='3').delete()
	"""if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		user_id= request.COOKIES['user_id']
		sponserId=check_secure_val(user_id)
		usr=User.objects.get(sponserId=sponserId)
		objs=treeGenerate(usr.sponserId)
		return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout,'objs':objs})
	else:
		return redirect('/')"""
	return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us'})

def products(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout})
	else:
		greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet})


def user_profile(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/user_profile.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout})
	else:
		return redirect('/')

def logout(request):
	greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
	# response=render(request, 'home/index.html', {'home':'#page-top','about':'#about','products':'#products','contact':'#contact','greet':greet}) 
	response=redirect('/')
	response.set_cookie('user_id', '')
	return response

def contact(request):
	form_class = ContactForm

	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get('contact_name', '')
			contact_email = request.POST.get('contact_email', '')
			contact_subject = request.POST.get('contact_subject', '')
			form_content = request.POST.get('content','')


			#to_email = [contact_email]
			#from_email = settings.EMAIL_HOST_USER
			#enquiry_message = """New contact form submission"""
			#send_mail(subject = contact_subject, from_email= from_email, recipient_list = to_email, message = enquiry_message, fail_silently = False)


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
			email.send(fail_silently=False)
			return redirect('contact')
	return render(request,'home/contact.html', {'form': form_class,})






