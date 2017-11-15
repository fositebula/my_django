#coding=utf-8
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")# project_name 项目名称
django.setup()

import requests

from job_collector.models import CollectInfos

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor

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
    buildinfo = rs.content
    buildinfo_list = set(buildinfo.split('\n'))
    try:
        buildinfo_list.remove('')
    except KeyError:
        print(buildinfo_list)
    for info in buildinfo_list:
        key, value = info.split(':', 1)
        info_dict[key] = value.strip()
    return info_dict



def get_repository(verify_url):
    data = parse_buildinfo_log(verify_url)
    print(data)

    changeids = data['CHANGES'].split(',')
    reops = []
    for i in changeids:
        assert i != ''
        rl = i.split(':')
        reops.append(rl[-2] + ":" + rl[-1])
    return "".join(reops)

def get_bugid(data):
    pass




def save_data(data):
    received_data = eval(data)
    repos = get_repository(received_data['verify_url'])
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
    )
    db_data.save()

class JobCollcetorProtocol(Protocol):
    def connectionMade(self):
        print("server: connect successfully")
        self.transport.write("Hello, welcome server!")
    def dataReceived(self, data):
        print(data)
        save_data(data)
        self.transport.write("end")

class CollectorFactory(ServerFactory):
    protocol = JobCollcetorProtocol

    def __init__(self):
        self.something = "server something"


def main():
    factory = CollectorFactory()
    port = reactor.listenTCP(10000, factory, interface="10.0.70.31")

    reactor.run()

if __name__ == "__main__":
    main()
    print("end")
