# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_collector', '0008_auto_20171113_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectinfos',
            name='device_type',
            field=models.CharField(max_length=50, verbose_name='device type'),
        ),
    ]
