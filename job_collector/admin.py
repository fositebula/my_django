# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from job_collector.models import CollectInfos, TestJob
# Register your models here.
admin.site.register(CollectInfos)
admin.site.register(TestJob)