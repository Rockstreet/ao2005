# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-08-01 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_category_code1c'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.TextField(default='', max_length=10000, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.TextField(default='', max_length=10000, verbose_name='Название'),
        ),
    ]
