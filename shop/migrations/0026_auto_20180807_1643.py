# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-08-07 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_remove_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.TextField(default='', verbose_name='Телефон'),
        ),
    ]
