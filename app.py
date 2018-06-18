#!/usr/bin/env python3
__author__ = "root202"
__copyright__ = "Copyright 2018, root202"
__credits__ = ["root202"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "root202"
__email__ = "root202@email.tg"
__status__ = "Development"

import argparse
import logging
import time
import uuid
from logging import handlers

import pygogo as gogo

import settings


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="specify the target",
                        type=str, required=True)
    parser.add_argument("-i", "--interval", help="specify the tip interval",
                        type=int, required=True)
    parser.add_argument("-m", "--interval_modulo",
                        help="specify second modulo to start the loop, i.e. at the 5th second"
                             ", etc... You know why this is useful.",
                        type=str, required=False, default=0)
    parser.add_argument("-tm", "--tip_message", help="specify the tip message",
                        type=str, required=False, default="")
    parser.add_argument("-a", "--amount", help="specify the tip amount, if jesse starts to change things up... -_-",
                        type=int, required=False, default=6)
    parser.add_argument("-u", "--username", help="the account username",
                        type=str, required=True)
    parser.add_argument("-p", "--password", help="the account password",
                        type=str, required=True)
    parser.add_argument("-l", "--token_limit", help="the max number of tokens to tip before exiting",
                        type=int, required=False, default=60)
    args = parser.parse_args()
    return args


def int_time():
    return int(time.time())

if __name__ == "main":
    total_tokens = 0
    args = handle_args()
    low_fmt = gogo.formatters.json_formatter
    high_fmt = logging.Formatter(gogo.formatters.FIXED_FORMAT)
    low_hdlr = logging.handlers.TimedRotatingFileHandler(settings.APP_SETTINGS["LOG_FILE"])
    high_hdlr = gogo.handlers.stdout_hdlr()
    logger = gogo.Gogo(settings.APP_SETTINGS["APP_NAME"], high_hdlr=high_hdlr, high_level='debug',
                       high_formatter=high_fmt,
                       low_formatter=low_fmt, low_hdlr=low_hdlr,
                       low_level=settings.APP_SETTINGS["LOG_LEVEL"]).get_logger()
    uuid_str = str(uuid.uuid4())
    logger.info("starting at {} with uuid {}".format(int_time(), uuid_str))

    try:
        #login, wait for chat to init, etc
        while int_time() % args.interval_modulo != 0:
            time.sleep(1)

        while total_tokens < args.token_limit:
            if int_time() % args.interval != 0:
                time.sleep(1)
                continue
            # do some magic, e.g. tip
    except KeyboardInterrupt:
        logger.info("shutting down at {}".format(int_time()))
        pass