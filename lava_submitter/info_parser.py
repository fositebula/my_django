#coding=utf-8

import os
from job_collector.models import CollectInfos, TestJob
from lava_submission.models import VerifyProjectInfo
import xmlrpclib
from lava_submitter.utils import download_image, decompress, get_image_url, get_image
from lava_submitter.JobData.android_data import AndroidData
from django.core.exceptions import ObjectDoesNotExist


def get_job_data(device_type, boot=None, system=None, userdata=None):
    job_data = AndroidData(device_type, boot=boot, system=system, userdata=userdata, job_name="lava_test_job")
    return job_data.get_data_str

def repository_to_image(verify_project_info, repo_l):
    """
        sprdlinux4.4--------------------------->boot
        sprduboot64_v201507 ------------------->u-boot
        sprdchipram16,sprdroid6.0_whale_dev --->u-boot-spl-16k
        sprd_trusty --------------------------->tos
        arm-trusted-firmware------------------->sml
    """
    image_name = []
    ch_repos = verify_project_info.repositorycheckitem_set.all()
    print(ch_repos)
    print(repo_l)
    for repo in repo_l:
        for ch_repo in ch_repos:
            if ch_repo.repo_name in repo:
                image_name.append(ch_repo.image_name)
    return image_name


def get_images(repo_image_list, local_path):
    image_paths = {}
    for image_type in repo_image_list:
        image_paths[image_type] = get_image(image_type, local_path).encode('utf-8')
    print(image_paths)
    return image_paths

class Submitter(object):
    def __init__(self, branch_project_info, job_data):
        self.lava_server_ip = branch_project_info.device_in_server.server_ip
        self.lava_server_user = branch_project_info.device_in_server.submit_user_name
        self.lava_server_token = branch_project_info.device_in_server.submit_user_token
        self.device_type = branch_project_info.device_type
        self.job_data = job_data
        pass

    def _get_lava_server(self):
        server = xmlrpclib.ServerProxy("http://%s:%s@%s/RPC2" % (
            self.lava_server_user,
            self.lava_server_token,
            self.lava_server_ip))
        return server

    def submit_job(self):
        server = self._get_lava_server()
        jobid = server.scheduler.submit_job(self.job_data)
        return jobid


class InfoParse(object):
    def __init__(self, source, reactor, info):
        self.reactor = reactor
        self.source = source
        self.info = info

    def _parse_info(self):
        try:
            branch_project_info = VerifyProjectInfo.objects.get(
                branch_project_info__branch_name=self.info.branch,
                branch_project_info__project_name=self.info.project
            )
        except ObjectDoesNotExist:
            self.info.filted = True
            self.info.submitted_result = CollectInfos.SUBMITTED_FAILED
            self.info.submitted_fail_reason = "The info not in the submit white list!"
            self.info.save()
            print("Did not fond the white list")
            return

        repo_l = self.info.repository.split(",")
        print(repo_l)
        repo_l = list(set(repo_l))
        repo_tl = repository_to_image(branch_project_info, repo_l)
        print("repo list:", repo_tl)
        if len(repo_tl) == 0:
            self.info.verify_project_info = branch_project_info
            self.info.filted = True
            self.info.submitted_result = CollectInfos.SUBMITTED_FAILED
            self.info.submitted_fail_reason = "The info's repository not in the submit white's info repository!"
            self.info.save()
            print("It's repository do not in white list info's repository!")
            return

        #下载image文件
        print("123",branch_project_info)
        url = get_image_url(self.info.branch, self.info.project, self.info.verify_url)
        print(url)
        f = download_image(url)
        path = decompress(f)

        info_data = get_images(repo_tl, path)
        print(info_data)
        #将测试信息合成yaml文件
        device_type = branch_project_info.device_type.name
        android_data = AndroidData(info_data, device_type.encode('utf-8'))
        yaml_str = android_data.get_data_str()
        print(yaml_str)
        #调用submit提交job
        submitter = Submitter(branch_project_info, yaml_str)
        jobid = submitter.submit_job()
        #保存提交后的信息
        self.info.verify_project_info = branch_project_info
        self.info.device_type = device_type
        self.info.submitted_result = CollectInfos.SUBMITTED_SUCCESSFULLY
        self.info.status = CollectInfos.SUBMITTED
        self.info.save()
        test_job = TestJob(jobid=jobid, collect_infos=self.info)
        test_job.save()
        print("submit successfully, jobid:%s"%jobid)
    def start(self):
        self._parse_info()
    pass
