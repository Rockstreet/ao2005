# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-20 12:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_item_offer_name2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='offer_name1',
        ),
        migrations.RemoveField(
            model_name='item',
            name='offer_name2',
        ),
    ]
