#coding=utf-8
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")
django.setup()
import logging
logging.basicConfig()

import time
import xmlrpclib
import datetime
from twisted.application.service import Service
from twisted.internet.task import LoopingCall
from check_lava_job_daemon.db_job_source import DatabaseJobIDSource, catchall_errback
from job_collector.models import CollectInfos, TestJob
from django.db.models import Q

RESUBMIT_MAX = 2

def get_lava_server(dbjob):
    username = dbjob.collect_infos.verify_project_info.device_in_server.submit_user_name
    hostname = dbjob.collect_infos.verify_project_info.device_in_server.server_hostname
    token = dbjob.collect_infos.verify_project_info.device_in_server.submit_user_token
    server = xmlrpclib.ServerProxy("http://%s:%s@%s/RPC2" % (username, token, hostname))
    return server

def get_case():
    pass
def get_case_result(dbjob, job_detail):
    pass

class JobCheck(object):
    def __init__(self, job):
        self.job = job

    def _get_server(self):
        self.server = get_lava_server(self.job)

    def _check_build_infos_status(self, job):
        buildid = job.collect_infos.buildid

        infos = CollectInfos.objects.filter(Q(buildid=buildid)
                                            & Q(last_job_status=CollectInfos.LAST_JOB_INCOMPLETE)
                                            & Q(filted=False)
                                            )

        if infos.count() != 0:
            #gerrit -1,如果提交的job中有一个job经过两次提交后还是incompolete，就给gerrit -1
            print("gerrit -1")
            return

        infos = CollectInfos.objects.filter(Q(buildid=buildid)
                                            & Q(last_job_status=CollectInfos.LAST_JOB_COMPLETE)
                                            & Q(filted=False)
                                            )
        #print(infos.count(), ":", infos[0].project_num)
        if infos.count() != 0:
            if infos.count() == int(infos[0].project_num):
                #gerrit +1,如果提交的job都是complete就给gerrit +1
                print("gerrit +1")
                return
        print("some jobs not complete")



    def start(self):
        self._get_server()
        #{'job_status': 'Complete', 'job_id': 200, 'bundle_sha1': ''}
        job_status = self.server.scheduler.job_status(self.job.jobid)
        print(job_status)
        if job_status['job_status'] == 'Incomplete':
            self.job.check_or_not = False
            if self.job.collect_infos.resubmit_count < RESUBMIT_MAX:
                re_jobid = self.server.scheduler.resubmit_job(self.job.jobid)
                self.job.collect_infos.resubmit_count += 1
                TestJob(jobid=re_jobid, collect_infos=self.job.collect_infos).save()
            elif self.job.collect_infos.resubmit_count == RESUBMIT_MAX:
                self.job.collect_infos.last_job_status = CollectInfos.LAST_JOB_INCOMPLETE
            self.job.collect_infos.save()

            self.job.end_time = datetime.datetime.fromtimestamp(
                time.mktime(self.server.scheduler.job_details(self.job.jobid)['end_time'].timetuple())
                            )
            get_case_result(self.job, self.server.scheduler.job_details(self.job.jobid))
            self.job.save()
        elif job_status['job_status'] == 'Complete':
            self.job.check_or_not = False
            self.job.collect_infos.last_job_status = CollectInfos.LAST_JOB_COMPLETE
            self.job.collect_infos.last_job_status = True
            self.job.collect_infos.save()
        else:
            get_case()
        self._check_build_infos_status(self.job)

class JobIDQueue(Service):

    def __init__(self, source, reactor):
        self.logger = logging.getLogger()
        self.source = source
        self.reactor = reactor
        self._check_job_call = LoopingCall(self._checkjob)
        self._check_job_call.clock = reactor

    def _checkjob(self):

        self.logger.debug("Refreshing jobs")
        return self.source.getJobList().addCallback(
            self._startJobs).addErrback(catchall_errback(self.logger))

    def _startJobs(self, jobs):
        for job in jobs:
            new_check_job = JobCheck(job)
            self.logger.info("job: %s ", new_check_job)

            new_check_job.start()

    def startService(self):
        self.logger.info("\n\nJob checker starting\n\n")
        self._check_job_call.start(20)

    def stopService(self):
        self._check_job_call.stop()
        return None

if __name__ == '__main__':
    # Start scheduler service.
    source = DatabaseJobIDSource()
    from twisted.internet import reactor
    service = JobIDQueue(source, reactor)
    reactor.callWhenRunning(service.startService)  # pylint: disable=no-member
    reactor.run()
    print('end')