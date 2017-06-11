from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class User(models.Model):
    sponserId = models.CharField(max_length=10,primary_key=True)
    username = models.CharField(unique= True,max_length=20)
    password = models.CharField(max_length=50)
    plan = models.IntegerField()
    joiningDate = models.DateTimeField(
            default=timezone.now)
    amount = models.FloatField()

    def saveUser(self):
        # self.published_date = timezone.now()
        self.save()

class UserDetails(models.Model):
    username = models.ForeignKey(User,to_field='username')#foreign key
    phoneNo = PhoneNumberField()
    address = models.TextField()
    email = models.EmailField()

    def saveDetails(self):
        # self.published_date = timezone.now()
        self.save()

class UserAccount(models.Model):
    username = models.ForeignKey(User,to_field='username')#foreign key
    accountNo = models.CharField(max_length=200)
    IFSCCode = models.CharField(max_length=200)
    holderName = models.CharField(max_length=100)
    bankName = models.CharField(max_length=200)
    accountType = models.BooleanField()
    panNo = models.CharField(max_length=200)

    def saveAccountDetails(self):
        # self.published_date = timezone.now()
        self.save()

class UserRelation(models.Model):
    sponserId = models.ForeignKey(User,to_field='username')
    parentId = models.CharField(max_length=10)
    lChild = models.CharField(max_length=10)
    rChild = models.CharField(max_length=10)
    level = models.IntegerField()
    def saveRelation(self):
        # self.published_date = timezone.now()
        self.save()

class Level(models.Model):
    level = models.IntegerField()
    count = models.IntegerField()
        