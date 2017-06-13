# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.contrib import admin
from .models import User
from .models import UserDetails
from .models import UserAccount
from .models import UserRelation
 
# Register your models here.
 
admin.site.register(User)	
admin.site.register(UserDetails)
admin.site.register(UserAccount)
admin.site.register(UserRelation)
