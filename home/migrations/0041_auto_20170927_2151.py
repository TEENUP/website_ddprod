# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-27 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_auto_20170917_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='modeOfPayment',
            field=models.CharField(default=b'AccountTransferCCAvenue', max_length=20),
        ),
        migrations.AddField(
            model_name='useraccountactual',
            name='modeOfPayment',
            field=models.CharField(default=b'AccountTransferCCAvenue', max_length=20),
        ),
    ]