from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

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

        