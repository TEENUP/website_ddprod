# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-17 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20170813_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialproduct',
            name='cashBackDescription',
            field=models.TextField(blank=True, null=True),
        ),
    ]
