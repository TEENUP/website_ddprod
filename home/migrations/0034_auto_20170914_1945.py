# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-14 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20170914_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normalproductsboughtlist',
            name='boughtDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='updated',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='specialproduct',
            name='timestamp',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='specialproduct',
            name='updated',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='joiningDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='joiningDate',
            field=models.DateField(null=True),
        ),
    ]