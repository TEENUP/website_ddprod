# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_auto_20170729_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRefferal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('sponserId', models.CharField(max_length=10)),
            ],
        ),
    ]
