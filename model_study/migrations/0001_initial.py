# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('age', models.IntegerField(default=0, verbose_name='age')),
            ],
        ),
    ]
