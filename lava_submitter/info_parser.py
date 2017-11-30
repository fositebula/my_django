#coding=utf-8

import os
from job_collector.models import CollectInfos, TestJob
from lava_submission.models import VerifyProjectInfo
import platform
python_version = platform.python_version()
if python_version.startswith('2.'):
    import xmlrpclib
    PYTHON_VERSION = 2
elif python_version.startswith('3.'):
    import xmlrpc.client
    PYTHON_VERSION = 3

from lava_submitter.utils import download_image, decompress, get_image_url, get_image
from lava_submitter.JobData.android_data import AndroidData
from django.core.exceptions import ObjectDoesNotExist


import logging
import logging.handlers

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.handlers.RotatingFileHandler("log/info_parser.log", maxBytes=1024*1024, backupCount=5)
handler.setFormatter(fmt=formatter)
logger = logging.getLogger(__name__+'.info_parser')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


from django.db import connection
from django.db import transaction

MAX_RETRIES = 3

def _commit_transaction(src=None):
    if connection.in_atomic_block:
        return
    for retry in range(MAX_RETRIES):
        try:
            transaction.commit()
            logger.debug('%s transaction committed', src)
            break
        except Exception as err:
            logger.warn('retrying transaction %s', err)
            continue


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
    logger.debug(ch_repos)
    logger.debug(repo_l)
    for repo in repo_l:
        for ch_repo in ch_repos:
            if ch_repo.repo_name in repo:
                image_name.append(ch_repo.image_name)
    return image_name


def get_images(repo_image_list, local_path):
    image_paths = {}
    for image_type in repo_image_list:
        image_paths[image_type] = get_image(image_type, local_path)
    logger.debug(image_paths)
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
        if PYTHON_VERSION == 2:
            server = xmlrpclib.ServerProxy("http://%s:%s@%s/RPC2" % (
                self.lava_server_user,
                self.lava_server_token,
                self.lava_server_ip))
        else:
            server = xmlrpc.client.ServerProxy("http://%s:%s@%s/RPC2" % (
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
            _commit_transaction(src='_parse_infoa')
            logger.debug("Did not fond the white list")
            return

        repo_l = self.info.repository.split(",")
        logger.debug(repo_l)
        repo_l = list(set(repo_l))
        repo_tl = repository_to_image(branch_project_info, repo_l)
        logger.debug( repo_tl)
        if len(repo_tl) == 0:
            self.info.verify_project_info = branch_project_info
            self.info.filted = True
            self.info.submitted_result = CollectInfos.SUBMITTED_FAILED
            self.info.submitted_fail_reason = "The info's repository not in the submit white's info repository!"
            self.info.save()
            _commit_transaction(src='_parse_infob')
            logger.debug("It's repository do not in white list info's repository!")
            return

        #下载image文件
        logger.debug(branch_project_info)
        url = get_image_url(self.info.branch, self.info.project, self.info.verify_url)
        logger.debug(url)
        f = download_image(url)
        path = decompress(f)

        logger.debug(path)
        info_data = get_images(repo_tl, path)
        logger.debug(info_data)
        #将测试信息合成yaml文件
        device_type = branch_project_info.device_type.name
        android_data = AndroidData(info_data, device_type)
        yaml_str = android_data.get_data_str()
        logger.debug(yaml_str)
        #调用submit提交job
        submitter = Submitter(branch_project_info, yaml_str)
        jobid = submitter.submit_job()
        #保存提交后的信息
        self.info.verify_project_info = branch_project_info
        self.info.device_type = device_type
        self.info.submitted_result = CollectInfos.SUBMITTED_SUCCESSFULLY
        self.info.status = CollectInfos.SUBMITTED
        self.info.save()
        _commit_transaction(src='_parse_infoc')
        test_job = TestJob(jobid=jobid, collect_infos=self.info)
        test_job.save()
        _commit_transaction(src='_parse_infod')
        logger.debug("submit successfully, jobid:%s"%jobid)
    def start(self):
        self._parse_info()
    pass
