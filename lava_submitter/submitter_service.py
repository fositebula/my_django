import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")
django.setup()
import logging
logging.basicConfig()

from twisted.application.service import Service
from twisted.internet.task import LoopingCall

from lava_submitter.info_parser import InfoParse
from lava_submitter.db_source import catchall_errback,DatabaseJobSource



class InfosQueue(Service):

    def __init__(self, source, reactor):
        self.logger = logging.getLogger()
        self.source = source
        self.reactor = reactor
        self._check_job_call = LoopingCall(self._checkinfos)
        self._check_job_call.clock = reactor

    def _checkinfos(self):

        self.logger.debug("Refreshing jobs")
        return self.source.getInfoList().addCallback(
            self._startJobs).addErrback(catchall_errback(self.logger))

    def _startJobs(self, infos):
        for info in infos:
            new_info = InfoParse(self.source, self.reactor, info)
            self.logger.info("info: %s ", info)

            new_info.start()

    def startService(self):
        self.logger.info("\n\nLAVA Scheduler starting\n\n")
        self._check_job_call.start(20)

    def stopService(self):
        self._check_job_call.stop()
        return None

if __name__ == '__main__':
    # Start scheduler service.
    source = DatabaseJobSource()
    from twisted.internet import reactor
    service = InfosQueue(source, reactor)
    reactor.callWhenRunning(service.startService)  # pylint: disable=no-member
    reactor.run()
    print('end')