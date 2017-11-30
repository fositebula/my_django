#coding=utf-8

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")# project_name 项目名称
django.setup()

import logging
import signal
from django.db import connection
from django.db import transaction
from django.db.utils import DatabaseError
from django.utils import timezone

from twisted.internet.threads import deferToThread  # pylint: disable=unused-import


from job_collector.models import CollectInfos


from zope.interface import (
    implements,
    Interface,
)

logger = logging.getLogger(__name__)

def catchall_errback(logger):
    def eb(failure):
        logger.error(
            '%s: %s\n%s', failure.type.__name__, failure.value,
            failure.getTraceback())
    return eb


# class IInfoSource(Interface):
#
#     def getInfoList():
#         """Get the list of collected information from verify server."""
#
#
#     def infoSubmitted(submitted_status):
#         """Mark the information submitted."""


MAX_RETRIES = 2


try:
    from MySQLdb import InterfaceError, OperationalError
except ImportError:
    class InterfaceError(Exception):
        pass

    class OperationalError(Exception):
        pass


class DatabaseJobSource(object):
    """ Deprecated """

    # implements(IInfoSource)

    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.DatabaseInfoSource')

    deferToThread = staticmethod(deferToThread)

    def deferForDB(self, func, *args, **kw):
        def wrapper(*args, **kw):
            transaction.set_autocommit(False)
            try:
                if connection.connection is None:
                    connection.cursor().close()
                    assert connection.connection is not None
                try:
                    return func(*args, **kw)
                except (DatabaseError, OperationalError, InterfaceError) as error:
                    message = str(error)
                    if message == 'connection already closed' or message.startswith(
                            'terminating connection due to administrator command') or message.startswith(
                                'could not connect to server: Connection refused'):
                        self.logger.warning(
                            'Forcing reconnection on next db access attempt')
                        if connection.connection:
                            if not connection.connection.closed:
                                connection.connection.close()
                            connection.connection = None
                    raise
            finally:
                # We don't want to leave transactions dangling under any
                # circumstances so we unconditionally issue a rollback.  This
                # might be a teensy bit wasteful, but it wastes a lot less time
                # than figuring out why your database migration appears to have
                # got stuck...
                transaction.rollback()
                transaction.set_autocommit(True)
        return self.deferToThread(wrapper, *args, **kw)

    def _commit_transaction(self, src=None):
        if connection.in_atomic_block:
            return
        for retry in range(MAX_RETRIES):
            try:
                transaction.commit()
                self.logger.debug('%s transaction committed', src)
                break
            except Exception as err:
                self.logger.warn('retrying transaction %s', err)
                continue

    def _kill_canceling(self, job):
        """
        Kills any remaining lava-dispatch processes via the pgid in the jobpid file

        :param job: the TestJob stuck in Canceling
        """
        pidrecord = os.path.join(job.output_dir, "jobpid")
        if os.path.exists(pidrecord):
            with open(pidrecord, 'r') as f:
                pgid = int(f.read())
                self.logger.info("Signalling SIGTERM to process group: %d", pgid)
                try:
                    os.killpg(pgid, signal.SIGTERM)
                except OSError as e:
                    self.logger.info("Unable to kill process group %d: %s", pgid, e)
                    os.unlink(pidrecord)

    def getJobList_impl(self):
        """
        This method is called in a loop by the scheduler daemon service.
        It's goal is to return a list of jobs that are ready to be started.
        Note: handles both old and pipeline jobs but only so far as putting
        devices into a Reserved state. Running pipeline jobs from Reserved
        is the sole concern of the dispatcher-master.
        """
        my_infos = CollectInfos.objects.filter(
            status=CollectInfos.NO_SUBMIT,
            filted=False,
        )

        if not connection.in_atomic_block:
            self._commit_transaction(src='getInfosList_impl')
        print("###", my_infos)
        return my_infos

    def getInfoList(self):
        return self.deferForDB(self.getJobList_impl)

    def startSubmit_impl(self, infos):
        for info in infos:
            info.status = CollectInfos.SUBMITTED
            info.submit_time = timezone.now()
            info.status = CollectInfos.SUBMITTED
            info.save()
            self._commit_transaction(src='startSubmit_impl')
        return infos

    def startedSubmit(self, info):
        return self.deferForDB(self.startSubmit_impl, info)