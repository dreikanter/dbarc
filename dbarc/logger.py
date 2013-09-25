# coding: utf-8

import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
import os
import os.path

# Logger message format
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"

# Logger message timestamp format
LOG_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

LOG_BACKUP_CNT = 3

LOG_MAX_BYTES = 1024 * 1024

_logger = None


def init(log_file=None, syslog=False, verbose=False):
    global _logger
    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG)

    def add_channel(channel, verbose):
        formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
        channel.setLevel(logging.DEBUG if verbose else logging.INFO)
        channel.setFormatter(formatter)
        _logger.addHandler(channel)

    # console channel
    add_channel(logging.StreamHandler(), verbose=False)

    # file channel
    if log_file is not None:
        try:
            os.makedirs(os.path.dirname(log_file))
        except FileExistsError:
            pass
        channel = RotatingFileHandler(log_file,
                                      maxBytes=LOG_MAX_BYTES,
                                      backupCount=LOG_BACKUP_CNT)
        add_channel(channel, verbose=verbose)

    # syslog channel
    if syslog:
        try:
            add_channel(SysLogHandler(address='/dev/log'), verbose=verbose)
        except Exception as e:
            _logger.error("error adding syslog handler: %s" % str(e))


def debug(message):
    _logger.debug(message)


def info(message):
    _logger.info(message)


def warn(message):
    _logger.warn(message)


def error(message):
    _logger.error(message)


def fatal(message):
    _logger.fatal(message)
