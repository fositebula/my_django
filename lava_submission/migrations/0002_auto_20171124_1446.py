# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lava_submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositorycheckitem',
            name='repo_name',
            field=models.CharField(max_length=100, verbose_name='repository name'),
        ),
    ]
