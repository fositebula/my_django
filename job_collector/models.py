# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lava_submission.models import VerifyProjectInfo

# Create your models here.
class CollectInfos(models.Model):

    NO_SUBMIT = 0
    SUBMITTED = 1

    STATUS_CHOICE = (
        (NO_SUBMIT, "No submit"),
        (SUBMITTED, "Submitted"),
    )

    STATUS_MAP={
        "No submit": NO_SUBMIT,
        "Submitted": SUBMITTED
    }

    SUBMITTED_SUCCESSFULLY = 0
    SUBMITTED_FAILED = 1

    SUBMITTED_CHOICE = (
        (SUBMITTED_SUCCESSFULLY, "Submitted successfully"),
        (SUBMITTED_FAILED, "Submitted failed"),
    )

    LAST_JOB_NO_STATUS = 0
    LAST_JOB_INCOMPLETE = 1
    LAST_JOB_COMPLETE = 2

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
    bugid = models.CharField('bugid to gerrit', max_length=200)
    repository = models.CharField('code repository', max_length=100)

    device_type = models.CharField('device type', max_length=50)

    from_verify_server_time =models.DateTimeField(auto_now=True)
    submit_time = models.DateTimeField(
        verbose_name=u"submit time",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        editable=False
    )

    status = models.IntegerField(
        verbose_name=u'submit status',
        default=NO_SUBMIT, choices=STATUS_CHOICE
    )

    filted = models.BooleanField(default=False)

    submitted_result = models.IntegerField(
        verbose_name=u'submitted result',
        help_text=u'submitted task can be successfully or fail',
        default=SUBMITTED_SUCCESSFULLY, choices=SUBMITTED_CHOICE,
    )
    submitted_fail_reason = models.CharField(
        verbose_name='submitted fail reason',
        help_text=u'submitted fail reason, if fail you can input some words mark it',
        max_length=100,
    )

    verify_project_info = models.ForeignKey(VerifyProjectInfo, null=True)
    resubmit_count = models.IntegerField(verbose_name=r'resubmit count', default=1)
    last_job_status = models.IntegerField(verbose_name=u'last lava job status', default=LAST_JOB_NO_STATUS)

    def __str__(self):
        return "%s---%s---%s---%s"%(self.buildid, self.branch, self.project, self.gerrit_id)

class TestJob(models.Model):
    #['Submitted' | 'Running' | 'Complete' | 'Incomplete' | 'Canceled' | 'Canceling']

    jobid = models.CharField(verbose_name='jobid', max_length=10, default=None)
    job_status = models.CharField(
        verbose_name='job status',
        default="Submitted",
        max_length=50
    )
    testcase = models.CharField(
        help_text=u"formate ${casename},${casename}",
        verbose_name='buildid', max_length=200, default="default"
    )
    testcase_result = models.CharField(
        help_text=u"formate ${casename},${result}",
        verbose_name=u"testcase result", max_length=200, default="default"
    )
    submitted_time = models.DateTimeField(verbose_name='submitted time', auto_now=True)
    end_time = models.DateTimeField(verbose_name='end time', null=True)

    collect_infos = models.ForeignKey('CollectInfos', null=True)
    check_or_not = models.BooleanField(verbose_name='Check job or not', default=True)

    def __str__(self):
        return "TestJob: %s"%self.jobid