# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-13 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item_variation',
            name='item',
        ),
        migrations.AlterField(
            model_name='item_image',
            name='item_variation',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Item'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Item'),
        ),
        migrations.DeleteModel(
            name='Item_variation',
        ),
    ]
