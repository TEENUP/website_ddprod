# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-15 16:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_auto_20170915_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'product/images/')),
                ('featured', models.BooleanField(default=False)),
                ('thumbnail', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateField(default=datetime.date.today, verbose_name=b'Date')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='specialproduct',
            name='productId',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Product'),
        ),
    ]
