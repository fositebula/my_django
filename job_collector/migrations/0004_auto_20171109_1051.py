# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_collector', '0003_collectinfos_submit_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectinfos',
            name='submit_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]