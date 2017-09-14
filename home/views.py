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

from django.views.decorators.csrf import csrf_exempt
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

# matching query for product
from django.shortcuts import get_object_or_404

#### CCAVENUE payment gateway dependencies/libraries and Functions

from Crypto.Cipher import AES
import md5
from string import Template

### 32 bit alphanumeric key and Access Code in quotes provided by CCAvenues.
accessCode = 'AVDV72EI95AN77VDNA' 	
workingKey = 'F29369319A53923B0415DE92C49FCD15'
 
def pad(data):
	length = 16 - (len(data) % 16)
	data += chr(length)*length
	return data

def encrypt(plainText,workingKey):
	iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
	plainText = pad(plainText)
	encDigest = md5.new ()
	encDigest.update(workingKey)
	enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
	encryptedText = enc_cipher.encrypt(plainText).encode('hex')
	return encryptedText



def decrypt(cipherText,workingKey):
	iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
	decDigest = md5.new ()
	decDigest.update(workingKey)
	encryptedText = cipherText.decode('hex')
	dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
	decryptedText = dec_cipher.decrypt(encryptedText)
	return decryptedText

# def res(encResp):
# 	'''
# 	Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.
# 	'''	 
# 	workingKey = 'F29369319A53923B0415DE92C49FCD15'
# 	decResp = decrypt(encResp,workingKey)
# 	data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'	
# 	data = data + decResp.replace('=','</td><td>')
# 	data = data.replace('&','</td></tr><tr><td>')
# 	data = data + '</td></tr></table>'
	
# 	# html = '''\
# 	# <html>
# 	# 	<head>
# 	# 		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
# 	# 		<title>Response Handler</title>
# 	# 	</head>
# 	# 	<body>
# 	# 		<center>
# 	# 			<font size="4" color="blue"><b>Response Page</b></font>
# 	# 			<br>
# 	# 			$response
# 	# 		</center>
# 	# 		<br>
# 	# 	</body>
# 	# </html>
# 	# '''
# 	# fin = Template(html).safe_substitute(response=data)
# 	# return fin
# 	return render(request, 'home/ccavResponseHandler.html', {'Response':data})





### Regular Expressions for dataEntries

regexForSponserId="^[A-Z0-9]*$"
regexForEmail = "^a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
regexForPanCard = "^[A-Z]{5}[0-9]{4}[A-Z]$"
regexForMobileNumber ="^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
regexForAadharCard = "^\d{4}\s\d{4}\s\d{4}$"
regexForUserName = "^[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$"
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
	parentObj=UserAccount.objects.get(sponserId=rootSponserId)
	childObj=UserAccount.objects.get(sponserId=sponserId)
	amountAdd=0
	#parentObj.amount+=(childObj.plan)*0.1
	#parentObj.saveUser()
	#print parentObj.amount

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

	spProd = SpecialProduct.objects.all()
	prod = Product.objects.all()


	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/index.html', {'home':'#page-top','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'spProd':spProd,'prod':prod})
	else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return render(request, 'home/index.html', {'home':'#page-top','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'spProd':spProd,'prod':prod})

def validateSponserId(sponserId):
	if len(sponserId)!=6:
		return False
	isValid = not not re.match(regexForSponserId,sponserId)
	if not isValid:
		return False
	else:
		user=UserAccount.objects.filter(sponserId=sponserId)
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
def validateUsername2(username):
	isUserNameValid = not not re.match(regexForUserName,username)
	if not isUserNameValid:
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
		# isEmailValid = validateEmail(emailFrom)
		# errorEmail = ""
		# if(not isEmailValid):
		# 	errorEmail = "Please Enter A valid Email Id"

		emailTo= [settings.EMAIL_HOST_USER]
		send_mail(subject,message,emailFrom,emailTo,fail_silently=False)
		return redirect('/thanks')
		
	else:	
		if isLoggedIn(request):
			# usr=User.objects.get(sponserId=sponserId)
			greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
			logout='<a class="page-scroll" href="/logout">Logout</a>'
			# Can take email and name
			return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout})#,'errorEmail':errorEmail})
		else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return render(request, 'home/contact_us.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet})



def sign_up(request):
	if request.method == "POST":
		
		username=request.POST.get('userName')
		isUsernameValid = validateUsername(username)
		errorUsername=""
		if(not isUsernameValid):
			errorUsername="User Already Exists"
		# isUsernameValid = validateUsername2(username)
		# errorUsername=""
		# if(not isUsernameValid):
		# 	errorName="User Name is not appropriate it must contain one character and alphanumneric and it must not contain any spaces"

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
		city = request.POST.get('city')
		state = request.POST.get('state')
		pinCode = request.POST.get('pinCode')
		
		#validation
		if isUsernameValid and isPasswordValid and isPhoneNumberValid:
			h_password=make_pw_hash(username,password)
			User.objects.create(username=username,password=h_password)
			UserDetails.objects.create(username=username,firstName=firstName,lastName=lastName, phoneNo=phoneNo,email=email,address=address,city=city,state=state,pinCode=pinCode)
			id_to_send=make_secure_val(str(username))
			response = redirect('/')
			response.set_cookie('user_id', id_to_send)
			return response
		else:
			# Render The page with errors
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','errorUsername':errorUsername,'errorPassword':errorPassword, 'errorPhoneNumber':errorPhoneNumber})#,'errorName':errorName})
	else:
		if isLoggedIn(request):
			return redirect('/')
		else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			# print options
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet})


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
				print "qwertyqwerty" + user_id
				id_to_send=make_secure_val(str(user_id))
				print "asdsasdsad" + id_to_send
				response = redirect('/myHome')
				response.set_cookie('user_id', id_to_send)
				return response
			else:

				# Incorrect Password But Write Incorrect Username OR password
				return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','name':username,'password':password,'errorLogin':errorLogin})
		else:
			# Incorrect Username but Write Incorrect Username OR password
				return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','name':username,'password':password,'errorLogin':errorLogin})

		

		# return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up'}) #{'home':'/','about':'/about_us','products':'/products','contact':'/contact_us','signup':'/sign_up'}) 
	else:
		if isLoggedIn(request):
			return redirect('/')
		else:
			greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return render(request, 'home/login.html',{'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet})

def about_us(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/about_us.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout})
	else:
		greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		return render(request, 'home/about_us.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet})


def dashboard(request):
	# parentId='1'
	# childObj=UserRelation.objects.create(sponserId='3',parentId='1')
	# User.objects.create(sponserId='3',username='rishabhdtu',amount=10000.00,password="asd",plan=1000)

	# insertUser(parentId,childObj)
	# UserRelation.objects.filter(sponserId='3').delete()
	# User.objects.filter(sponserId='3').delete()
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		user_id= request.COOKIES['user_id']
		username=check_secure_val(user_id)
		print username
		usr=User.objects.get(username=username)
#changed sponserId to username
		refferal=UserRefferal.objects.filter(username=username)
		accounts=UserAccount.objects.filter(username=username)
		print refferal
		children = UserRelation.objects.filter(parentUsername=username)
		print children
		# if refferal.count()>0:
		# 	refferal=UserRefferal.objects.filter(username=username)
		# 	reff = []
		# 	for refs in refferal:
		# 		objs=treeGenerate(refs.sponserId)
		# 		listOfUserObjects=[]
		# 		listOfUserDetailsObjects=[]
		# 		for obj in objs:
		# 			print obj
		# 			sid,pid=obj.sponserId,obj.parentId
		# 			print sid
		# 			print pid
		# 			u=User.objects.get(sponserId=sid)
		# 			print u
		# 			ud=UserDetails.objects.get(username=u.username)
		# 			print ud
		# 			listOfUserObjects.append(u)
		# 			listOfUserDetailsObjects.append(ud)
		# 		objsTemp=[listOfUserObjects,listOfUserDetailsObjects]
		# 		print objsTemp
		# 		temp=[]
		# 		for i in range(0,len(objsTemp[0])):
		# 			t=[]
		# 			t.append(objsTemp[1][i].firstName)
		# 			t.append(objsTemp[1][i].lastName)
		# 			t.append(objsTemp[1][i].username)
		# 			t.append(objsTemp[0][i].plan)
		# 			t.append(objsTemp[1][i].email)
		# 			temp.append(t)
		# 		reff.append(temp)	
			
			#return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'temp':temp,'user':usr,'num':len(objs),'reff':refferal,'relation':objs})
		#else:
		return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':usr,'reff':refferal,'relation':children,'accounts':accounts})


	else:
		return redirect('/')
	# return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'})

def products(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		user_id= request.COOKIES['user_id']
		username=check_secure_val(user_id)
		print username
		usr=User.objects.get(username=username)
#changed sponserId to username
		refferal=UserRefferal.objects.filter(username=username)
		print refferal
		children = UserRelation.objects.filter(parentUsername=username)
		print children
		# if refferal.count()>0:
		# 	refferal=UserRefferal.objects.filter(username=username)
		# 	reff = []
		# 	for refs in refferal:
		# 		objs=treeGenerate(refs.sponserId)
		# 		listOfUserObjects=[]
		# 		listOfUserDetailsObjects=[]
		# 		for obj in objs:
		# 			print obj
		# 			sid,pid=obj.sponserId,obj.parentId
		# 			print sid
		# 			print pid
		# 			u=User.objects.get(sponserId=sid)
		# 			print u
		# 			ud=UserDetails.objects.get(username=u.username)
		# 			print ud
		# 			listOfUserObjects.append(u)
		# 			listOfUserDetailsObjects.append(ud)
		# 		objsTemp=[listOfUserObjects,listOfUserDetailsObjects]
		# 		print objsTemp
		# 		temp=[]
		# 		for i in range(0,len(objsTemp[0])):
		# 			t=[]
		# 			t.append(objsTemp[1][i].firstName)
		# 			t.append(objsTemp[1][i].lastName)
		# 			t.append(objsTemp[1][i].username)
		# 			t.append(objsTemp[0][i].plan)
		# 			t.append(objsTemp[1][i].email)
		# 			temp.append(t)
		# 		reff.append(temp)	
			
			#return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'temp':temp,'user':usr,'num':len(objs),'reff':refferal,'relation':objs})
		#else:
		return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':usr,'reff':refferal,'relation':children})


	else:
		return redirect('/')
	# return render(request, 'home/dashboard.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'})
	#return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','buy':'/buy'})
	"""if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/dashboard">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','buy':'/buy','greet':greet,'logout':logout})
	else:
		greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		return render(request, 'home/products.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','buy':'/buy','greet':greet})

"""

def user_profile(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		user_id= request.COOKIES['user_id']
		username=check_secure_val(user_id)
		user=User.objects.get(username=username)
		userDetails=UserDetails.objects.get(username=user.username)
		accountDetails=UserAccount.objects.filter(username=username)
		if accountDetails.count()>0:
			userAccount=UserAccount.objects.filter(username=username)
			reff = UserRefferal.objects.filter(username=username)
			if reff.count()>0:	
				refferal=UserRefferal.objects.filter(username=user.username)
				return render(request, 'home/user_profile.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':user,'userDetails':userDetails,'userAccount':userAccount[0],'refferal':refferal})
			else:
				return render(request, 'home/user_profile.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':user,'userDetails':userDetails,'userAccount':userAccount[0]})
		else:
			return render(request, 'home/user_profile.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':user,'userDetails':userDetails})
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
		greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		# Logout link
		return render(request, 'home/thanks.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout})
	else:
		greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		return render(request, 'home/thanks.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet})

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

##### CCAvenues RequestHandler

# def login_buy():
# 	p_merchant_id = "147110"
# 	p_order_id = sponserId
# 	p_currency = "INR"
# 	p_amount = spPrice
# 	p_redirect_url = "http://192.168.2.49:8085/ccavResponseHandler"
# 	p_cancel_url = "http://192.168.2.49:8085/ccavResponseHandler"
# 	p_language = "EN"
# 	p_billing_name = "userDetails.firstName" + "userDetails.lastName"
# 	p_billing_address = "userDetails.address"
# 	p_billing_city = "Delhi"
# 	p_billing_state = "Delhi"
# 	p_billing_zip = "110085"
# 	p_billing_country = "India"
# 	p_billing_tel = "userDetails.phoneNo"
# 	p_billing_email = "userDetails.email"
# 	p_delivery_name = "userDetails.firstName" + "userDetails.lastName"
# 	p_delivery_address = "userDetails.address"
# 	p_delivery_city = "Delhi"
# 	p_delivery_state = "Delhi"
# 	p_delivery_zip = "110085"
# 	p_delivery_country = "India"
# 	p_delivery_tel ="userDetails.phoneNo"
# 	p_merchant_param1 = "userDetails.email"
# 	p_merchant_param2 = ""
# 	p_merchant_param3 = ""
# 	p_merchant_param4 = ""
# 	p_merchant_param5 = ""
#  	p_promo_code = ""
# 	p_customer_identifier = ""
	
	

# 	merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+p_delivery_name+'&'+'delivery_address='+p_delivery_address+'&'+'delivery_city='+p_delivery_city+'&'+'delivery_state='+p_delivery_state+'&'+'delivery_zip='+p_delivery_zip+'&'+'delivery_country='+p_delivery_country+'&'+'delivery_tel='+p_delivery_tel+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&'
		
# 	encryption = encrypt(merchant_data,workingKey)

# 	html = '''\
# <html>
# <head>
# 	<title>Sub-merchant checkout page</title>
# 	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
# </head>
# <body>
# <form id="nonseamless" method="post" name="redirect" action="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction"/> 
# 		<input type="hidden" id="encRequest" name="encRequest" value=$encReq>
# 		<input type="hidden" name="access_code" id="access_code" value=$xscode>
# 		<script language='javascript'>document.redirect.submit();</script>
# </form>    
# </body>
# </html>
# '''
# 	fin = Template(html).safe_substitute(encReq=encryption,xscode=accessCode)
			
# 	return fin	

def buy(request):
	#you have to write view for adding product into the user
	#return render(request, 'home/thanks.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'})

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
			return render(request, 'home/sign_up.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','errorSponserId':errorSponserId,'errorUsername':errorUsername,'errorPassword':errorPassword, 'errorPhoneNumber':errorPhoneNumber, 'errorPanNumber':errorPanNumber,'errorAdharNumber':errorAdharNumber})
	'''
	# x = request.GET.get("q",None)
	# #print x
	# #spProd = SpecialProduct.objects.get(productId = x)
	# spProd = get_object_or_404(SpecialProduct, productId=x)
	# print spProd
	# spPrice = spProd.price
	# monthlyCashBack = spPrice
	# parentRecieveAfterRefferal = spPrice
	

	if request.method == "POST":

		
		parentId=request.POST.get('sponserId')
		#print "1"+parentId
		isSponserIdValid=validateSponserId(parentId)
		print isSponserIdValid
		errorSponserId=""
		if (not isSponserIdValid):
			errorSponserId="Invalid Sponser Id"

		pUsername = UserAccount.objects.get(sponserId=parentId)
		sponserId="".join(random.choice(string.ascii_uppercase+string.digits) for x in range (0,6))
		#print "2"+ sponserId
		# username=request.POST.get('userName')
		# isUsernameValid = validateUsername(username)
		# errorUsername=""
		# if(not isUsernameValid):
		# 	errorUsername="User Already Exists"

		# password=request.POST.get('password')
		# confirmPassword=request.POST.get('confirmPassword')

		# isPasswordValid = validatePassword(password,confirmPassword)
		# errorPassword=""
		# if(not isPasswordValid):
		# 	errorPassword="Passwords didn't match"

		#product = request.POST.get('product')
		#print "4"+product
		# firstName= request.POST.get('firstName')
		# lastName=request.POST.get('lastName')
		
		# phoneNo=request.POST.get('mobNumber')
		# # print phoneNo
		# isPhoneNumberValid = validateMobileNumber(phoneNo)
		# errorPhoneNumber = ""
		# if(not isPhoneNumberValid):
		# 	errorPhoneNumber = "Invalid Phone Number"
		# else:
		# 	phoneNo='+91'+phoneNo

		# email= request.POST.get('email')		
		# address= request.POST.get('address')
		spProd = request.POST.get('product')
		spPrice = request.POST.get('amount')

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
		print isPanNumberValid
		errorPanNumber= ""
		if(not isPanNumberValid):
			errorPanNumber = "Invalid Pan Number"

		aadhaarCard = request.POST.get('aadhaarCard')
		
		aadhaarNo = request.POST.get('aadhaarCardNumber')
		isAadharNumberValid = validateAadharCard(aadhaarNo)
		print isAadharNumberValid
		errorAdharNumber = ""
		if(not isAadharNumberValid):
			errorAdharNumber = "Invalid Aadhar Number"
		

		#validation
		if isSponserIdValid:
			# h_password=make_pw_hash(username,password)
			# User.objects.create(sponserId=sponserId,username=username,password=h_password, plan=product,amount=0.00)
			# UserDetails.objects.create(username=username,firstName=firstName,lastName=lastName, phoneNo=phoneNo,email=email,address=address)
			
#cookies for username
			user_id= request.COOKIES['user_id']
			#print "6 "+ user_id
			username=check_secure_val(user_id)
			userDetails = UserDetails.objects.get(username=username)
			print "5"+ username
			#return redirect('/')
			print "hello world???"

			UserRefferal.objects.create(username=username,sponserId=sponserId)
			UserAccount.objects.create(firstName=userDetails.firstName,lastName=userDetails.lastName,phoneNo=userDetails.phoneNo,address=userDetails.address,email=userDetails.email,sponserId=sponserId,username=username,holderName=holderName,IFSCCode=IFSCCode,bankName=bankName,branchName=branchName,
				accountType=accountType,accountNo=accountNo,panNo=panNo,aadhaarNo=aadhaarNo,productId=spProd,amount=spPrice)
			UserRelation.objects.create(childUsername=username,sponserId=sponserId,parentUsername=pUsername.username,parentId=parentId)
			# Payment
			insertUser(parentId,sponserId)
			#set Cookie
			# redirect to homepage
			id_to_send=make_secure_val(str(sponserId))
#link payment gateway over here under insert user
### CCAVenues Payment Gateway 
			p_merchant_id = "147110"
			p_order_id = sponserId
			p_currency = "INR"
			p_amount = spPrice
			p_redirect_url = "https://www.petalsart.in/ccavResponseHandler/"
			p_cancel_url = "https://www.petalsart.in/ccavResponseHandler/"
			p_language = "EN"
			p_billing_name = userDetails.firstName + ' ' + userDetails.lastName
			p_billing_address = userDetails.address
			p_billing_city = userDetails.city
			p_billing_state = userDetails.state
			p_billing_zip = ""
			p_billing_country = "India"
			#p_billing_tel = userDetails.phoneNo
			p_billing_email = userDetails.email
			p_delivery_name = userDetails.firstName + ' ' + userDetails.lastName
			p_delivery_address = userDetails.address
			p_delivery_city = userDetails.city
			p_delivery_state = userDetails.state
			p_delivery_zip = ""
			p_delivery_country = "India"
			#p_delivery_tel =userDetails.phoneNo
			p_merchant_param1 = userDetails.email
			p_merchant_param2 = ""
			p_merchant_param3 = ""
			p_merchant_param4 = ""
			p_merchant_param5 = ""
 			p_promo_code = ""
			p_customer_identifier = ""
	
	

			merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+p_delivery_name+'&'+'delivery_address='+p_delivery_address+'&'+'delivery_city='+p_delivery_city+'&'+'delivery_state='+p_delivery_state+'&'+'delivery_zip='+p_delivery_zip+'&'+'delivery_country='+p_delivery_country+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&'
		
			encryption = encrypt(merchant_data,workingKey)

			# html = '''\
			# <html>
			# <head>
			# <title>Sub-merchant checkout page</title>
			# <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
			# </head>
			# <body>
			# <form id="nonseamless" method="post" name="redirect" action="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction"/> 
			# <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
			# <input type="hidden" name="access_code" id="access_code" value=$xscode>
			# <script language='javascript'>document.redirect.submit();</script>
			# </form>    
			# </body>
			# </html>
			# '''
			#fin = Template(html).safe_substitute(encReq=encryption,xscode=accessCode)
			
			#return fin

			return render(request, 'home/payment.html', {'encReq':encryption,'xscode':accessCode})














			
			# print "ID TO SEND"+id_to_send
			# print "SPONSERID"+sponserId
			response = redirect('/') ##uncomment it afterwards
			#response.set_cookie('user_id', id_to_send)
			#return render(request, 'home/buy.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','errorSponserId':errorSponserId,'errorPanNumber':errorPanNumber,'errorAdharNumber':errorAdharNumber,'spProd':spProd})
			return response ##uncomment it afterwards
		else:
			# x = request.GET.get("q",None)
			# #print x
			# #spProd = SpecialProduct.objects.get(productId = x)
			# spProd = get_object_or_404(SpecialProduct, productId=x)
			# print spProd
			# spPrice = spProd.price
			# monthlyCashBack = spPrice
			# parentRecieveAfterRefferal = spPrice
			# Render The page with errors
			# options='<select name="product" class="form-control"><option selected="selected" disabled>PRODUCTS</option><option value="5000">5000</option>'
			# options+='<option value="10000">10000</option><option value="10000">30000</option>'
			# options+='<option value="10000">50000</option><option value="10000">90000</option></select>'
			return render(request, 'home/buy.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','errorSponserId':errorSponserId,'errorPanNumber':errorPanNumber,'errorAdharNumber':errorAdharNumber})#,'spProd':spProd})
	else:
		if not isLoggedIn(request):
			#greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return redirect('/sign_up')
		else:
			print "my name is puneet"
			x = request.GET.get("q",None)
			print x
			
			spProd = get_object_or_404(SpecialProduct, productId=x)
			print spProd
			#spProd = SpecialProduct.objects.get(productId = x)
			spPrice = spProd.price
			print spPrice
			monthlyCashBack = spPrice
			parentRecieveAfterRefferal = spPrice 
			
			
		# 	# if prod=='1':
		# 	# 	options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000" selected="selected">5000</option>'
		# 	# 	options+='<option value="10000">10000</option><option value="30000">30000</option>'
		# 	# 	options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
		# 	# elif prod=='2':
		# 	# 	options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
		# 	# 	options+='<option value="10000" selected="selected">10000</option><option value="30000">30000</option>'
		# 	# 	options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
		# 	# elif prod=='3':
		# 	# 	options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
		# 	# 	options+='<option value="10000">10000</option><option value="30000" selected="selected">30000</option>'
		# 	# 	options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
		# 	# elif prod=='4':
		# 	# 	options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
		# 	# 	options+='<option value="10000">10000</option><option value="30000">30000</option>'
		# 	# 	options+='<option value="50000" selected="selected">50000</option><option value="90000">90000</option></select>'
		# 	# elif prod=='5':
		# 	# 	options='<select name="product" class="form-control"><option disabled>PRODUCTS</option><option value="5000">5000</option>'
		# 	# 	options+='<option value="10000">10000</option><option value="30000">30000</option>'
		# 	# 	options+='<option value="50000">50000</option><option value="90000" selected="selected">90000</option></select>'
		# 	# else:
		# 	# 	options='<select name="product" class="form-control"><option selected="selected" disabled>PRODUCTS</option><option value="5000">5000</option>'
		# 	# 	options+='<option value="10000">10000</option><option value="30000">30000</option>'
		# 	# 	options+='<option value="50000">50000</option><option value="90000">90000</option></select>'
		# 	# greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
		# 	# print options
			return render(request, 'home/buy.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','spProd':spProd})
			#return render(request, 'home/buy.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'})
		
@csrf_exempt	
def ccavResponseHandler(request):
	if request.method == "POST":
		plainText = request.POST.get('encResp')
		workingKey = 'F29369319A53923B0415DE92C49FCD15'
		decResp = decrypt(plainText,workingKey)
		data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'	
		data = data + decResp.replace('=','</td><td>')
		data = data.replace('&','</td></tr><tr><td>')
		data = data + '</td></tr></table>'

		print "gateway"
		print plainText
		return render(request, 'home/ccavResponseHandler.html', {'Response':decResp})
		


	#return render(request,'home/buy.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'})


def buyProducts(request):
	# if not isLoggedIn(request):
	# 		#greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
	# 		return redirect('/sign_up')
	# else:

	# 	x = request.GET.get("q",None)
	# 	product = Product.objects.get(productId = x)


	# 	p_merchant_id = "147110"
	# 	p_order_id = product.productId
	# 	p_currency = "INR"
	# 	p_amount = product.price
	# 	p_redirect_url = "https://www.petalsart.in/ccavResponseHandler/"
	# 	p_cancel_url = "https://www.petalsart.in/ccavResponseHandler/"
	# 	p_language = "EN"
	# 	p_billing_name = "userDetails.firstName" + ' ' + "userDetails.lastName"
	# 	p_billing_address = "userDetails.address"
	# 	p_billing_city = "Delhi"
	# 	p_billing_state = "Delhi"
	# 	p_billing_zip = "110085"
	# 	p_billing_country = "India"
	# 	#p_billing_tel = userDetails.phoneNo
	# 	p_billing_email = "userDetails.email"
	# 	p_delivery_name = "userDetails.firstName + userDetails.lastName"
	# 	p_delivery_address = "userDetails.address"
	# 	p_delivery_city = "Delhi"
	# 	p_delivery_state = "Delhi"
	# 	p_delivery_zip = "110085"
	# 	p_delivery_country = "India"
	# 	#p_delivery_tel =userDetails.phoneNo
	# 	p_merchant_param1 = "userDetails.email"
	# 	p_merchant_param2 = ""
	# 	p_merchant_param3 = ""
	# 	p_merchant_param4 = ""
	# 	p_merchant_param5 = ""
 # 		p_promo_code = ""
	# 	p_customer_identifier = ""
	
	

	# 	merchant_data="1049"
		
	# 	encryption = encrypt(merchant_data,workingKey)

	# 	return render(request, 'home/payment.html', {'encReq':encryption,'xscode':accessCode})


	# 	# return render(request,'home/buyProducts.html',{'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','product':product})
	#you have to write view for adding product into the user
	#return render(request, 'home/thanks.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'})

	if request.method == "POST":
		x = request.POST.get('product-title')
	 	product = Product.objects.get(title = x)
		mobile = request.POST.get('mobileNo')
		price = request.POST.get('amount')

		
		
		if x==product.title:
#link payment gateway over here under insert user
### CCAVenues Payment Gateway 
			user_id= request.COOKIES['user_id']
			#print "6 "+ user_id
			username=check_secure_val(user_id)
			userDetails = UserDetails.objects.get(username=username)

			p_merchant_id = "147110"
			p_order_id = username
			p_currency = "INR"
			p_amount = price
			p_redirect_url = "https://www.petalsart.in/ccavResponseHandler/"
			p_cancel_url = "https://www.petalsart.in/ccavResponseHandler/"
			p_language = "EN"
			p_billing_name = userDetails.firstName + ' ' + userDetails.lastName
			p_billing_address = userDetails.address
			p_billing_city = userDetails.city
			p_billing_state = userDetails.state
			p_billing_zip = ""
			p_billing_country = "India"
			#p_billing_tel = userDetails.phoneNo
			p_billing_email = userDetails.email
			p_delivery_name = userDetails.firstName + ' ' + userDetails.lastName
			p_delivery_address = userDetails.address
			p_delivery_city = userDetails.city
			p_delivery_state = userDetails.state
			p_delivery_zip = ""
			p_delivery_country = "India"
			#p_delivery_tel =userDetails.phoneNo
			p_merchant_param1 = userDetails.email
			p_merchant_param2 = ""
			p_merchant_param3 = ""
			p_merchant_param4 = ""
			p_merchant_param5 = ""
 			p_promo_code = ""
			p_customer_identifier = ""
	
	

			merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+'&'
			encryption = encrypt(merchant_data,workingKey)

			return render(request, 'home/payment.html', {'encReq':encryption,'xscode':accessCode})
		else:
			return render(request, 'home/buyProducts.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up'})
	else:
		if not isLoggedIn(request):
			#greet='<a class="page-scroll" href="/sign_up">Sign Up</a>'
			return redirect('/sign_up')
		else:
			x = request.GET.get("q",None)
			product = Product.objects.get(productId = x)

			return render(request, 'home/buyProducts.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','signup':'/sign_up','product':product})
			#return render(request, 'home/buy.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'})
		

def slide(request):
	return render(request, 'home/slide.html')
	

def TermsAndConditions(request):
	return render(request, 'home/TermsAndConditions.html')

def paymentGateway(request):
	return render(request, 'home/paymentGateway.html')

def popup(request):
	return render(request, 'home/popup.html')

def myHome(request):
	if isLoggedIn(request):
		# usr=User.objects.get(sponserId=sponserId)
		greet='<a class="page-scroll" href="/myHome">Dashboard</a>'
		logout='<a class="page-scroll" href="/logout">Logout</a>'
		user_id= request.COOKIES['user_id']
		username=check_secure_val(user_id)
		user=User.objects.get(username=username)
		userDetails=UserDetails.objects.get(username=user.username)
		accountDetails=UserAccount.objects.filter(username=username)
		if accountDetails.count()>0:
			userAccount=UserAccount.objects.filter(username=username)
			reff = UserRefferal.objects.filter(username=username)
			if reff.count()>0:	
				refferal=UserRefferal.objects.filter(username=user.username)
				return render(request, 'home/myHome.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':user,'userDetails':userDetails,'userAccount':userAccount[0],'refferal':refferal})
			else:
				return render(request, 'home/myHome.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':user,'userDetails':userDetails,'userAccount':userAccount[0]})
		else:
			return render(request, 'home/myHome.html', {'home':'/','about':'/about_us','products':'/all','contact':'/contact_us','greet':greet,'logout':logout,'user':user,'userDetails':userDetails})
	else:
		return redirect('/')


#Product APP 
def all(request):
	products = Product.objects.all()
	#primaryImages = Product.objects.all()
	specialProduct = SpecialProduct.objects.all()
	context = {'showProducts': products,'specialProduct': specialProduct,'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'} #"primaryImages": primaryImages}
	template = 'home/all.html'
	return render (request, template, context)

def single(request):
		x = request.GET.get("q",None)
		print x
		product = Product.objects.get(productId = x)
		#spProd = SpecialProduct.objects.get(productId = x)
		#print spProd
		print product

		images = product.productimage_set.all()
		#images = ProductImage.objects.filter(product=product)
		#images1 = roduct.objects.filter(product=product)

		context = {'product':product,'images':images,'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'}
		template = 'home/single.html'
		return render (request, template, context) 

def singles(request):
		x = request.GET.get("q",None)
		print "aaaaaaaaaaaaa" + x
		#product = Product.objects.get(productId = x)
		spProd = SpecialProduct.objects.get(productId = x)
		print spProd
		#print product

		#images = product.productimage_set.all()
		#images = ProductImage.objects.filter(product=product)
		#images1 = roduct.objects.filter(product=product)

		context = {'spProd':spProd,'home':'/','about':'/about_us','products':'/all','contact':'/contact_us'}
		template = 'home/singles.html'
		return render (request, template, context) 