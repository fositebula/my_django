# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_collector', '0003_collectinfos_buildid_from_where'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectinfos',
            name='buildid_from_where',
            field=models.IntegerField(default=0, verbose_name='buildid from debug or ci'),
        ),
    ]
