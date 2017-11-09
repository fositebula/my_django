# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CollectInfos(models.Model):
    branch = models.CharField('branch', max_length=50)
    project = models.CharField('project', max_length=50)
    buildid = models.CharField('buildid', max_length=50)
    submiter = models.CharField('submiter', max_length=50)
    verify_url = models.CharField('verify_url', max_length=200)
    gerrit_id = models.CharField('gerrit_id', max_length=50)
    port = models.CharField('port', max_length=50)
    compile_user = models.CharField('compile_user', max_length=50)
    module = models.CharField('module', max_length=50)
    testcase = models.CharField('testcase', max_length=50)
    manual_testcase = models.CharField('manual_testcase', max_length=50)
    phone_number = models.CharField('phone_number', max_length=50)
    test_description = models.CharField('test_description', max_length=50)
    project_num = models.CharField('project_num', max_length=50)
    test_task_type = models.CharField('test_task_type', max_length=50)

    def __str__(self):
        return "%s---%s---%s---%s"%(self.buildid, self.branch, self.project, self.gerrit_id)