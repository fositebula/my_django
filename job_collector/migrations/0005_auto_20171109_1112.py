# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_collector', '0004_auto_20171109_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectinfos',
            name='status',
            field=models.IntegerField(choices=[('No submit', 0), ('Submitted', 1)], default=0, verbose_name='submit status'),
        ),
        migrations.AddField(
            model_name='collectinfos',
            name='submitted_fail_reason',
            field=models.CharField(default=None, help_text='submitted fail reason, if fail you can input some words mark it', max_length=100, verbose_name='submitted fail reason'),
        ),
        migrations.AddField(
            model_name='collectinfos',
            name='submitted_result',
            field=models.IntegerField(choices=[('Submitted successfully', 0), ('Submitted failed', 1)], default=0, help_text='submitted task can be successfully or fail', verbose_name='submitted result'),
        ),
    ]
