# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-07-13 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20180627_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='in_stock',
            field=models.IntegerField(default=0, verbose_name='Количество на складе'),
        ),
    ]
