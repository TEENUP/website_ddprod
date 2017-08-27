# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
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
	date_hierarchy = 'joiningDate'#'timestamp' #updated
	search_fields = ['username']
	list_display = ['username','joiningDate','amount']
	#list_editable = ['username']
	list_filter = ['username','joiningDate']
    
	#readonly_fields = ['username','amount','password','joiningDate']
	#prepopulated_fields = {"slug": ("title",)}
	class Meta:
		model = User

def export_csv(modeladmin, request, queryset):
    	import csv
    	from django.utils.encoding import smart_str
    	response = HttpResponse(content_type='text/csv')
    	response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    	writer = csv.writer(response, csv.excel)
    	response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    	writer.writerow([
    	    smart_str(u"username"),
    	    smart_str(u"sponserId"),
    	    smart_str(u"panNo"),
    	    smart_str(u"aadharNo"),
    	    smart_str(u"amount"),
            smart_str(u"bankName"),
            smart_str(u"IFSCCode"),
            smart_str(u"branchName"),
            smart_str(u"accountNumber"),
            smart_str(u"DateOfJoning"),
    	])
    	for obj in queryset:
    	    writer.writerow([
    	        smart_str(obj.username),
    	        smart_str(obj.sponserId),
    	        smart_str(obj.panNo),
    	        smart_str(obj.aadhaarNo),
    	        smart_str(obj.amount),
                smart_str(obj.bankName),
                smart_str(obj.IFSCCode),
                smart_str(obj.branchName),
                smart_str(obj.accountNo),
                smart_str(obj.joiningDate),

    	    ])
    	return response
export_csv.short_description = u"Export CSV"

class userAccountsAdmin(admin.ModelAdmin):
    date_hierarchy = 'joiningDate'
    search_fields = ['username','sponserId']
    actions = [export_csv]
    list_display = ('username','sponserId','accountNo','IFSCCode','amount','joiningDate')
    list_filter = ('username','joiningDate')

    #readonly_fields = ['username','sponserId','accountNo','IFSCCode','holderName','bankName','branchName','accountType','panNo','aadhaarNo','amount','joiningDate']

class userDetailsAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['username']
    list_filter = ['username']

    #readonly_fields = ['username','firstName','lastName','phoneNo','address','email']

class userRefferalAdmin(admin.ModelAdmin):
    search_fields = ['sponserId', 'username']
    list_display = ['username','sponserId']
    list_filter = ['username','sponserId']

    #readonly_fields = ['username','sponserId']

class userRelationAdmin(admin.ModelAdmin):
    search_fields = ['childUsername','parentUsername']
    list_display = ['childUsername','parentUsername']
    list_filter = ['childUsername','parentUsername','sponserId','parentId']

    #readonly_fields = ['childUsername','sponserId','parentUsername','parentId']


admin.site.site_header = 'Petals Art Jewellery Administration'
admin.site.register(User, userAdmin)	
admin.site.register(UserDetails, userDetailsAdmin)
admin.site.register(UserAccount, userAccountsAdmin)
admin.site.register(UserRelation, userRelationAdmin)
admin.site.register(Product)
admin.site.register(SpecialProduct)
admin.site.register(ProductImage)
admin.site.register(UserRefferal, userRefferalAdmin)


