# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-13 13:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_specialproduct_cashback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='aadhaarCard',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='panCard',
        ),
    ]