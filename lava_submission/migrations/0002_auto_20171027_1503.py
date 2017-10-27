# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lava_submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifyprojectinfo',
            name='device_type',
            field=models.CharField(choices=[('V', 'verify'), ('D', 'daily'), ('M', 'manual')], max_length=50, verbose_name='Device Type'),
        ),
    ]
