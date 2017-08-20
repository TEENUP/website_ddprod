# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.contrib import admin
from .models import User
from .models import UserDetails
from .models import UserAccount
from .models import UserRelation
from .models import Product
from .models import SpecialProduct
from .models import ProductImage
from .models import UserRefferal

 
# Register your models here.
class userAdmin(admin.ModelAdmin):
	#date_hierarchy = 'timestamp' #updated
	search_fields = ['username']
	#list_display = ['title','price','active','updated']
	#list_editable = ['price', 'active']
	#list_filter = ['price','active']
	#readonly_fields = ['updated','timestamp']
	#prepopulated_fields = {"slug": ("title",)}
	# class Meta:
	# 	model = User

class userAccountsAdmin(admin.ModelAdmin):
	search_fields = ['username','sponserId']

class userDetailsAdmin(admin.ModelAdmin):
	search_fields = ['username']

class userRefferalAdmin(admin.ModelAdmin):
	search_fields = ['sponserId', 'username']

class userRelationAdmin(admin.ModelAdmin):
	search_fields = ['childUsername','parentUsername']






admin.site.site_header = 'Petals Art Jewellery Administration'
admin.site.register(User, userAdmin)	
admin.site.register(UserDetails, userDetailsAdmin)
admin.site.register(UserAccount, userAccountsAdmin)
admin.site.register(UserRelation, userRelationAdmin)
admin.site.register(Product)
admin.site.register(SpecialProduct)
admin.site.register(ProductImage)
admin.site.register(UserRefferal, userRefferalAdmin)


