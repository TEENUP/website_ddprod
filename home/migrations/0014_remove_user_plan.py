# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-22 09:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20170722_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='plan',
        ),
    ]