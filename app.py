#!/usr/bin/env python3
__author__ = "root202"
__copyright__ = "Copyright 2018, root202"
__credits__ = ["root202"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "root202"
__email__ = "root202@email.tg"
__status__ = "Development"

import logging
import uuid
from logging import handlers
from socket import gethostbyname
import pygogo as gogo

import settings

low_fmt = gogo.formatters.json_formatter
high_fmt = logging.Formatter(gogo.formatters.FIXED_FORMAT)
low_hdlr = logging.handlers.TimedRotatingFileHandler(settings.APP_SETTINGS["LOG_FILE"])
high_hdlr = gogo.handlers.stdout_hdlr()
logger = gogo.Gogo(settings.APP_SETTINGS["APP_NAME"], high_hdlr=high_hdlr, high_level='debug',
                   high_formatter=high_fmt,
                   low_formatter=low_fmt, low_hdlr=low_hdlr,
                   low_level=settings.APP_SETTINGS["LOG_LEVEL"]).get_logger()
uuid_str = str(uuid.uuid4())

if __name__ == "main":
    try:
        #do some magic
        pass
    except KeyboardInterrupt:
        pass
