# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20170716_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=29.99, max_digits=100)),
                ('primaryImage', models.ImageField(default=b'products/None/placeholderImage.png', upload_to=b'products/images1/')),
                ('secondaryImage', models.ImageField(default=b'products/None/placeholderImage.png', upload_to=b'products/images2/')),
                ('additionalImage', models.ImageField(default=b'products/None/placeholderImage.png', upload_to=b'products/images3/')),
                ('sales_price', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('productId', models.CharField(max_length=20, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('update_defaults', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='additionalImage',
            field=models.ImageField(default=b'products/None/placeholderImage.png', upload_to=b'products/images3/'),
        ),
        migrations.AddField(
            model_name='product',
            name='primaryImage',
            field=models.ImageField(default=b'products/None/placeholderImage.png', upload_to=b'products/images1/'),
        ),
        migrations.AddField(
            model_name='product',
            name='secondaryImage',
            field=models.ImageField(default=b'products/None/placeholderImage.png', upload_to=b'products/images2/'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=999, unique=True),
            preserve_default=False,
        ),
    ]
