#coding=utf-8

from job_collector.models import CollectInfos, TestJob
from lava_submission.models import VerifyProjectInfo

class InfoParse(object):
    def __init__(self, source, reactor, info):
        self.reactor = reactor
        self.source = source
        self.info = info

    def _parse_info(self):
        if VerifyProjectInfo.objects.filter(
            branch_project_info__branch_name=self.info.branch,
            branch_project_info__project_name=self.info.project
        ).count() == 0:
            self.info.filted = True
            self.info.submitted_result = CollectInfos.SUBMITTED_FAILED
            self.info.submitted_fail_reason = "The info not in the submit white list!"
            self.info.save()
            print("submit failed")
        else:
            #下载image文件
            #将测试信息合成yaml文件
            #调用submit提交job
            #保存提交后的信息
            print("submit successfully")
    def start(self):
        self._parse_info()
    pass
