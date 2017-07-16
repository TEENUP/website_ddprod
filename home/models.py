from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.core.urlresolvers import reverse

class User(models.Model):
    sponserId = models.CharField(max_length=10,primary_key=True)
    username = models.CharField(unique= False,max_length=20)
    password = models.CharField(max_length=1000,blank=True)
    plan = models.IntegerField(blank=True)
    joiningDate = models.DateTimeField(
            default=timezone.now,blank=True)
    amount = models.FloatField(blank=True)

    def saveUser(self):
        # self.published_date = timezone.now()
        self.save()

class UserDetails(models.Model):
    username = models.CharField(max_length=10)#foreign key
    firstName= models.CharField(max_length=100,default="Blank")
    lastName=models.CharField(max_length=100,default="Blank")
    phoneNo = PhoneNumberField()
    address = models.TextField()
    email = models.EmailField()

    def saveDetails(self):
        # self.published_date = timezone.now()
        self.save()

class UserAccount(models.Model):
    username = models.CharField(max_length=10)#foreign key
    accountNo = models.CharField(max_length=200)
    IFSCCode = models.CharField(max_length=200)
    holderName = models.CharField(max_length=100)
    bankName = models.CharField(max_length=200)
    branchName = models.CharField(max_length=200,default="Blank")
    accountType = models.BooleanField()
    panNo = models.CharField(max_length=200,default="Blank")
    aadhaarNo = models.CharField(max_length=200,default="Blank")
    panCard = models.BinaryField(default="Blank")
    aadhaarCard = models.BinaryField(default="Blank")
    photo = models.BinaryField(default="Blank")

    def saveAccountDetails(self):
        # self.published_date = timezone.now()
        self.save()

class UserRelation(models.Model):
    sponserId = models.CharField(max_length=10)
    parentId = models.CharField(max_length=10)

    def saveRelation(self):
        # self.published_date = timezone.now()
        self.save()

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=29.99)
    #category = models.ManyToManyField(Category, null=True, blank=True)
    sales_price = models.DecimalField(decimal_places=2, max_digits=100,\
                                                null=True, blank=True)
    #slug = models.SlugField(unique=True)
    productId = models.CharField(max_length=20, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    update_defaults = models.BooleanField(default=False)


    def saveProduct(self):
        self.save()

   
    """ def __unicode__(self):
        return self.title
    
    class Meta:
        unique_together = ('title', 'slug') 
    
    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse("single_product", kwargs={"slug": self.slug}) """
  


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.product.title        