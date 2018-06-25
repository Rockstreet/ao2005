# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-22 09:02
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20180620_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(default='', max_length=255, verbose_name='Название')),
                ('file', sorl.thumbnail.fields.ImageField(blank=True, upload_to='category', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
    ]
