# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-12 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_userrefferal'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialproduct',
            name='cashBack',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
