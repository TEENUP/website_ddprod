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
from django.shortcuts import render, Http404
# from django.template import RequestContext

from models import *
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
import re
from django.core.mail import send_mail
from django.conf import settings


regexForSponserId="^[A-Z0-9]*$"
regexForEmail = "^a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
regexForPanCard = "^[A-Z]{5}[0-9]{4}[A-Z]$"
regexForMobileNumber ="^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
regexForAadharCard = "^\d{4}\s\d{4}\s\d{4}$"
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

def validateMobileNumber(phoneNo):
	if len(phoneNo)!=10:
		return False
	isMobileNumberValid = not not re.match(regexForMobileNumber,phoneNo)
	if not isMobileNumberValid:
		return False
	return True

def validatePanCArd(panNo):
	if len(panNo)!=10:
		return False
	isPanCardValid = not not re.match(regexForPanCard,panNo)
	if not isPanCardValid:
		return False
	return True

def validateAadharCard(aadhaarNo):
	if len(aadhaarNo)!=12:
		return False
	isAadharCardValid = not not re.match(regexForAadharCard,aadhaarNo)
	if not isAadharCardValid:
		return False
	return True

def validateEmail(email):
	isEmailValid = not not re.match(regexForEmail,email)
	if not isEmailValid:
		return False
	return True


def validateUsername(username):
	user=User.objects.filter(username=username)
	if user.count()>0:
		return False
	return True

def validatePassword(password,confirmPassword):
	if password == confirmPassword:
		return True
	return False

def contact_us(request):
	if request.method == 'POST':
		subject= request.POST.get('subject')
		message= '%s %s' %(request.POST.get('message'),request.POST.get('name')+"("+request.POST.get('email')+")")
		emailFrom=request.POST.get('email')
		isEmailValid = validateEmail(emailFrom)
		errorEmail = ""
		if(not isEmailValid):
			errorEmail = "Please Enter A valid Email Id"

		emailTo= [settings.EMAIL_HOST_USER]
		send_mail(subject,message,emailFrom,emailTo,fail_silently=False)
		return redirect('/thanks')
		
	else:	
		if isLoggedIn(request):
			# usr=User.objects.get(sponserId=sponserId)
			greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
			logout='<a class="page-scroll" href="/logout">Logout</a>'
			# Can take email and name
			return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout,'errorEmail':errorEmail})
		else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,})



def sign_up(request):
	if request.method == "POST":
		
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

		firstName= request.POST.get('firstName')
		lastName=request.POST.get('lastName')
		
		phoneNo=request.POST.get('mobNumber')
		# print phoneNo
		isPhoneNumberValid = validateMobileNumber(phoneNo)
		errorPhoneNumber = ""
		if(not isPhoneNumberValid):
			errorPhoneNumber = "Invalid Phone Number"
		else:
			phoneNo='+91'+phoneNo

		email= request.POST.get('email')		
		address= request.POST.get('address')
		
		#validation
		if isUsernameValid and isPasswordValid:
			h_password=make_pw_hash(username,password)
			User.objects.create(username=username,password=h_password)
			UserDetails.objects.create(username=username,firstName=firstName,lastName=lastName, phoneNo=phoneNo,email=email,address=address)
			id_to_send=make_secure_val(str(username))
			response = redirect('/')
			response.set_cookie('user_id', id_to_send)
			return response
		else:
			# Render The page with errors
			options='<select name="product" class="form-control"><option selected="selected" disabled>PRODUCTS</option><option value="5000">5000</option>'
			options+='<option value="10000">10000</option><option value="10000">30000</option>'
			options+='<option value="10000">50000</option><option value="10000">90000</option></select>'
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up','errorUsername':errorUsername,'errorPassword':errorPassword, 'errorPhoneNumber':errorPhoneNumber,'selectOptions':options})
	else:
		if isLoggedIn(request):
			return redirect('/')
		else:
			prod=request.GET.get("productId",None)
			if prod=='1':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000" selected="selected">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			elif prod=='2':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000" selected="selected">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			elif prod=='3':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000" selected="selected">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			elif prod=='4':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000" selected="selected">50000</option><option value="90000">90000</option></select>'
			elif prod=='5':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000" selected="selected">90000</option></select>'
			else:
				options='<select name="product" class="form-control"><option selected="selected" disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			# print options
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'selectOptions':options})


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
				user_id=usr.username
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
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		user_id= request.COOKIES['user_id']
		sponserId=check_secure_val(user_id)
		usr=User.objects.get(sponserId=sponserId)
		objs=treeGenerate(usr.sponserId)
		listOfUserObjects=[]
		listOfUserDetailsObjects=[]
		for obj in objs:
			sid,pid=obj.sponserId,obj.parentId
			u=User.objects.get(sponserId=sid)
			ud=UserDetails.objects.get(username=u.username)
			listOfUserObjects.append(u)
			listOfUserDetailsObjects.append(ud)
		objsTemp=[listOfUserObjects,listOfUserDetailsObjects]
		temp=[]
		for i in range(0,len(objsTemp[0])):
			t=[]
			t.append(objsTemp[1][i].firstName)
			t.append(objsTemp[1][i].lastName)
			t.append(objsTemp[1][i].username)
			t.append(objsTemp[0][i].plan)
			t.append(objsTemp[1][i].email)
			temp.append(t)
		return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout,'temp':temp,'user':usr,'num':len(objs)})
	else:
		return redirect('/')
	# return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us'})

def products(request):
	return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','buyAnotherProduct':'/buyAnotherProduct'})
	"""if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','buyAnotherProduct':'/buyAnotherProduct','greet':greet,'logout':logout})
	else:
		greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','buyAnotherProduct':'/buyAnotherProduct','greet':greet})

"""

def user_profile(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		user_id= request.COOKIES['user_id']
		sponserId=check_secure_val(user_id)
		user=User.objects.get(sponserId=sponserId)
		userDetails=UserDetails.objects.get(username=user.username)
		userAccount=UserAccount.objects.get(username=user.username)
		return render(request, 'home/user_profile.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout,'user':user,'userDetails':userDetails,'userAccount':userAccount})

	else:
		return redirect('/')

def logout(request):
	greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
	# response=render(request, 'home/index.html', {'home':'#page-top','about':'#about','products':'#products','contact':'#contact','greet':greet}) 
	response=redirect('/')
	response.set_cookie('user_id', '')
	return response

def thanks(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/thanks.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'logout':logout})
	else:
		greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		return render(request, 'home/thanks.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'errorEmail':errorEmail})

"""
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
			#enquiry_message = New contact form submission
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



"""
def contact(request):
	form=ContactForm(request.POST or None)
	if form.is_valid():
		subject= form.cleaned_data['contact_subject']
		message= '%s %s' %(form.cleaned_data['cotent'],form.cleaned_data['contact_name'])
		emailFrom=form.cleaned_data['contact_email']
		emailTo= [settings.EMAIL_HOST_USER]

		send_mail(subject,message,emailFrom,emailTo,fail_silently=False)
		print form.cleaned_data['contact_email']
	context=locals()
	template='home/newContact.html'
	return render(request,template,context)


def buyAnotherProduct(request):
	#you have to write view for adding product into the user
	#return render(request, 'home/thanks.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us'})

	'''if request.method == "POST":
		parentId=request.POST.get('sponserId')
		isSponserIdValid=validateSponserId(parentId)
		errorSponserId=""
		if not isSponserIdValid:
			errorSponserId="Invalid Sponser Id"


	if isSponserIdValid:
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
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up','errorSponserId':errorSponserId,'errorUsername':errorUsername,'errorPassword':errorPassword, 'errorPhoneNumber':errorPhoneNumber, 'errorPanNumber':errorPanNumber,'errorAdharNumber':errorAdharNumber})
	'''
	'''if request.method == "POST":
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
		# print phoneNo
		isPhoneNumberValid = validateMobileNumber(phoneNo)
		errorPhoneNumber = ""
		if(not isPhoneNumberValid):
			errorPhoneNumber = "Invalid Phone Number"
		else:
			phoneNo='+91'+phoneNo

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
		isPanNumberValid = validatePanCArd(panNo)
		errorPanNumber= ""
		if(not isPanNumberValid):
			errorPanNumber = "Invalid Pan Number"

		aadhaarCard = request.POST.get('aadhaarCard')
		
		aadhaarNo = request.POST.get('aadhaarCardNumber')
		isAadharNumberValid = validateAadharCard(aadhaarNo)
		errorAdharNumber = ""
		if(not isAadharNumberValid):
			errorAdharNumber = "Invalid Aadhar Number"
		
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
			options='<select name="product" class="form-control"><option selected="selected" disabled>PRODUCTS</option><option value="5000">5000</option>'
			options+='<option value="10000">10000</option><option value="10000">30000</option>'
			options+='<option value="10000">50000</option><option value="10000">90000</option></select>'
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up','errorSponserId':errorSponserId,'errorUsername':errorUsername,'errorPassword':errorPassword, 'errorPhoneNumber':errorPhoneNumber, 'errorPanNumber':errorPanNumber,'errorAdharNumber':errorAdharNumber,'selectOptions':options})
	else:
		if isLoggedIn(request):
			return redirect('/')
		else:
			prod=request.GET.get("productId",None)
			if prod=='1':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000" selected="selected">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			elif prod=='2':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000" selected="selected">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			elif prod=='3':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000" selected="selected">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			elif prod=='4':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000" selected="selected">50000</option><option value="90000">90000</option></select>'
			elif prod=='5':
				options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000" selected="selected">90000</option></select>'
			else:
				options='<select name="product" class="form-control"><option selected="selected" disabled>PRODUCTS</option><option value="5000">5000</option>'
				options+='<option value="10000">10000</option><option value="30000">30000</option>'
				options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			# print options
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','greet':greet,'selectOptions':options})
			'''



	return render(request,'home/buyAnotherProduct.html', {'home':'/','about':'/about_us','products':'/products','contact':'/contact_us'})

def slide(request):
	return render(request, 'home/slide.html')
	





#Product APP 
def all(request):
	products = Product.objects.all()
	#primaryImages = Product.objects.all()
	context = {'products': products} #"primaryImages": primaryImages}
	template = 'home/all.html'
	return render (request, template, context)

def single(request):
		x = request.GET.get("q",None)
		print x
		product = Product.objects.get(productId = x)
		print product

		#images = product.productimage_set.all()
		images = ProductImage.objects.filter(product=product)
		context = {'product': product, "images": images}
		template = 'home/single.html'
		return render (request, template, context) 