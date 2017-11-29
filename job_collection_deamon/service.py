#coding=utf-8
import os,django
from os.path import join,dirname,abspath
import sys

PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0,PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")# project_name 项目名称
django.setup()

import requests

from job_collector.models import CollectInfos

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor

import platform
PYTHON_VERSION = platform.python_version()

import logging
import logging.handlers

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.handlers.RotatingFileHandler("log/job_collector.log", maxBytes=1024*1024, backupCount=5)
handler.setFormatter(fmt=formatter)
logger = logging.getLogger(__name__+'.job_collector')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


JOB_INFO_JSON = """
{
    "branch":"${branch}",
    "project":"${project}",
    "buildid":"${buildid}",
    "submiter":"${submiter}",
    "verify_url":"${verify_url}",
    "gerrit_id":"${gerrit_id}",
    "port":"${port}",
    "compile_user":"${compile_user}",
    "module":"${module}",
    "testcase":"${testcase}",
    "manual_testcase":"${manual_testcase}",
    "phone_number":"${phone_number}",
    "test_description":"${test_description}",
    "project_num":"${project_num}",
    "test_task_type":"${test_task_type}",
}
"""

def parse_buildinfo_log(verify_url):
    info_dict = {}
    buildinfo_url = verify_url + "/artifact/buildinfo.log"
    rs = requests.get(buildinfo_url)
    buildinfo = rs.content.decode()
    buildinfo_list = set(buildinfo.split('\n'))
    try:
        buildinfo_list.remove('')
    except KeyError:
        logger.error(buildinfo_list)
        #print(buildinfo_list)
    try:
        for info in buildinfo_list:
            if ':' in info:
                key, value = info.split(':', 1)
                info_dict[key] = value.strip()
    except Exception as e:
        logger.error(e)
    return info_dict



def get_repository(verify_url):
    data = parse_buildinfo_log(verify_url)
    #print(data)
    logger.debug(data)

    reops = []
    try:
        changeids = data['CHANGES'].split(',')
        logger.debug(changeids)
        #print("####",changeids)
        for i in changeids:
            if ':' in i:
                rl = i.split(':')
                reops.append(rl[-2] + ":" + rl[-1])
    except Exception as e:
        logger.error(e)
    return ",".join(reops)

def get_bugid(data):
    pass




def save_data(data):
    received_data = eval(data)
    repos = get_repository(received_data['verify_url'])
    logger.debug(repos)
    print(received_data)
    db_data = CollectInfos(

        branch=received_data['branch'],
        project=received_data['project'],
        buildid=received_data['buildid'],
        submiter=received_data['submiter'],
        verify_url=received_data['verify_url'],
        gerrit_id=received_data['gerrit_id'],
        port=received_data['port'],
        compile_user=received_data['compile_user'],
        module=received_data['module'],
        testcase=received_data['testcase'],
        manual_testcase=received_data['manual_testcase'],
        phone_number=received_data['phone_number'],
        test_description=received_data['test_description'],
        project_num=received_data['project_num'],
        test_task_type=received_data['test_task_type'],
        repository=repos,
        buildid_from_where=received_data['buildid_from_where']
    )
    db_data.save()

class JobCollcetorProtocol(Protocol):
    def connectionMade(self):
        #print("server: connect successfully")
        logger.info("server: connect successfully")
        self.transport.write("Hello, welcome server!".encode('utf-8'))
    def dataReceived(self, data):
        #print(data)
        logger.debug(data)
        save_data(data)
        self.transport.write("end".encode())

class CollectorFactory(ServerFactory):
    protocol = JobCollcetorProtocol

    def __init__(self):
        self.something = "server something"


def main():
    try:
        factory = CollectorFactory()
        port = reactor.listenTCP(10000, factory, interface="10.0.70.63")

        reactor.run()
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    main()
    print("end")
    logger.info('end')
