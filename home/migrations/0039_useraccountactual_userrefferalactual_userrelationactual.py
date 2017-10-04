# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-16 17:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_auto_20170915_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccountActual',
            fields=[
                ('username', models.CharField(max_length=20)),
                ('firstName', models.CharField(default=b'Blank', max_length=100)),
                ('lastName', models.CharField(default=b'Blank', max_length=100)),
                ('phoneNo', phonenumber_field.modelfields.PhoneNumberField(default=b'Blank', max_length=128)),
                ('address', models.TextField(default=b'Blank')),
                ('email', models.EmailField(default=b'Blank', max_length=254)),
                ('sponserId', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('accountNo', models.CharField(max_length=200)),
                ('IFSCCode', models.CharField(max_length=200)),
                ('holderName', models.CharField(max_length=100)),
                ('bankName', models.CharField(max_length=200)),
                ('branchName', models.CharField(default=b'Blank', max_length=200)),
                ('accountType', models.BooleanField()),
                ('panNo', models.CharField(default=b'Blank', max_length=200)),
                ('aadhaarNo', models.CharField(default=b'Blank', max_length=200)),
                ('amount', models.FloatField(blank=True, default=0)),
                ('joiningDate', models.DateField(default=datetime.date.today, verbose_name=b'Date')),
                ('productId', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserRefferalActual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('sponserId', models.CharField(max_length=10)),
                ('monthlyCashbackAmount', models.FloatField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserRelationActual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('childUsername', models.CharField(max_length=20)),
                ('sponserId', models.CharField(max_length=10)),
                ('parentUsername', models.CharField(max_length=20)),
                ('parentId', models.CharField(max_length=10)),
                ('cashRewardPrentWillRecieve', models.FloatField(blank=True, default=0)),
            ],
        ),
    ]