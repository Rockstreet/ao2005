# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-26 15:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_gallery', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='Video',
        ),
    ]
