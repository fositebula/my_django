# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class LavaServerInfo(models.Model):
    location = models.CharField('Location', max_length=20)
    server_hostname = models.CharField('Host Name', max_length=50)
    server_ip = models.GenericIPAddressField('Server IP Address', null=False, blank=False)
    submit_user_name = models.CharField('Submiter user name', max_length=30)
    submit_user_token = models.CharField('Submit user token', max_length=200)

    def __str__(self):
        if self.server_hostname:
            return "%s in %s"%(self.server_hostname, self.location)
        else:
            return "%s in %s"%(self.server_ip, self.location)

class VerifyProjectInfo(models.Model):
    branch_name = models.CharField('Branch Name', max_length=50)
    project_name = models.CharField('Project Name', max_length=50)
    managers_mail = models.EmailField('Email', max_length=254)
    task_type = models.CharField('Task Type', max_length=20)
    device_type = models.CharField('Device Type', max_length=50)
    stop_flag = models.BooleanField('Stopping Test', default=False)
    device_in_server = models.ForeignKey(LavaServerInfo)
    modify_date = models.DateField()

    def __str__(self):
        return "%s:%s" % (self.branch_name, self.project_name)
