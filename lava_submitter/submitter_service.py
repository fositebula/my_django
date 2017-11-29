import os,django
from os.path import join,dirname,abspath
import sys

PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0,PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")
django.setup()
import logging
import logging.handlers
#logging.basicConfig()

from twisted.application.service import Service
from twisted.internet.task import LoopingCall

from lava_submitter.info_parser import InfoParse
from lava_submitter.db_source import catchall_errback,DatabaseJobSource



class InfosQueue(Service):

    def __init__(self, source, reactor):
        self.logger = logging.getLogger(__name__+'.InfosQueue')
        self._init_logger()
        self.source = source
        self.reactor = reactor
        self._check_job_call = LoopingCall(self._checkinfos)
        self._check_job_call.clock = reactor

    def _init_logger(self):
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.handlers.RotatingFileHandler('log/InfosQueue.log', maxBytes=1024*1024, backupCount=5)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

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
        self.logger.info("\n\nInfosQueue starting\n\n")
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
