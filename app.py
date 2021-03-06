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
import time
import uuid
from logging import handlers

import configargparse
import pygogo as gogo
from selenium import webdriver

import settings


def handle_args():
    parser = configargparse.ArgParser()
    parser.add_argument("-t", "--host", help="specify the host",
                        type=str, required=True, env_var="HOST_USER")
    parser.add_argument("-i", "--interval", help="specify the tip interval",
                        type=int, required=True, env_var="TIP_INERVAL")
    parser.add_argument("-m", "--interval_modulo",
                        help="specify second modulo to start the loop, i.e. at the 5th second"
                             ", etc... You know why this is useful.",
                        type=str, required=False, default=0, env_var="INTERVAL_MODULO")
    parser.add_argument("-tm", "--tip_message", help="specify the tip message",
                        type=str, required=False,
                        default="brought to you via {}, a project by {}".format(settings.APP_SETTINGS["APP_NAME"],
                                                                                "root202"), env_var="")
    parser.add_argument("-a", "--amount", help="specify the tip amount, if jesse starts to change things up... -_-",
                        type=int, required=False, default=6, env_var="TIP_AMOUNT")
    parser.add_argument("-u", "--username", help="the account username",
                        type=str, required=True, env_var="CB_USERNAME")
    parser.add_argument("-p", "--password", help="the account password",
                        type=str, required=True, env_var="CB_PASSWORD")
    parser.add_argument("-l", "--token_limit", help="the max number of tokens to tip before exiting",
                        type=int, required=False, default=60, env_var="TOKEN_LIMIT")
    parser.add_argument("--selenium_host", help="the selenium grid host", type=str, required=True,
                        env_var="SEL_GRID_HOST")
    parser.add_argument("--selenium_port", help="the selenium grid port", type=int, default=4444,
                        env_var="SEL_GRID_PORT")
    parser.add_argument("--browser", help="the browser to use", default="chrome", env_var="SEL_GRIB_BROWSER")
    parser.add_argument("--defang", help="run without tipping", default=False, action="store_true",
                        env_var="TIP_DEFANG")
    parser.add_argument("--keep_browser_open", help="keep the browser open after hitting the token limit",
                        action="store_true", default=False)
    args = parser.parse_args()
    return args


def int_time():
    return int(time.time())


def get_elem(driver: webdriver.Remote, by, locator, timeout):
    found = 0
    if by not in ["id", "css", "class", "xpath"]:
        raise Exception("invalid by locator type passed to {}".format("get_elem"))
    start_time = int_time()
    while found == 0:
        time.sleep(1)
        if (int_time() - start_time) > timeout:
            raise TimeoutError("couldn't find element {}:{} in {}s".format(by, locator, timeout))
        if by == "id":
            elements = driver.find_elements_by_id(locator)
        if by == "css":
            elements = driver.find_elements_by_css_selector(locator)
        if by == "class":
            elements = driver.find_elements_by_class_name(locator)
        if by == "xpath":
            elements = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div/form/input[5]")
        if elements == None:
            logger.debug("no elements found, trying again...")
            continue
        found = len(elements)
        if found == 0:
            logger.debug("no elements found, trying again...")
    return elements[0]


def try_to_close_the_browser(args, logger, driver = None):
    if driver == None:
        pass
    if args.keep_browser_open == True:
        logger.info("keeping the browser open...")
        pass
    try:
        driver.close()
    except:
        pass

if __name__ == "__main__":
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
        logger.info("setting up selenium...")
        driver = webdriver.Remote(
            command_executor="http://{}:{}/wd/hub".format(args.selenium_host, args.selenium_port),
            desired_capabilities={
                "browserName": args.browser,
                "version": "latest"
            })

        logger.info("logging in...")

        driver.get("https://chaturbate.com/")

        logger.debug("clicking the entrance_terms div")
        elem = get_elem(driver, "id", "entrance_terms", 30)
        elem.click()

        logger.debug("clicking the close_entrance_terms button")
        elem = get_elem(driver, "id", "close_entrance_terms", 30)
        elem.click()

        logger.info("sleeping for 5...")
        time.sleep(5)

        logger.debug("clicking the login link")
        elem = get_elem(driver, "class", "login-link", 30)
        elem.click()

        logger.debug("filling out the username")
        elem = get_elem(driver, "id", "id_username", 30)
        elem.send_keys(args.username)

        logger.debug("filling out the password")
        elem = get_elem(driver, "id", "id_password", 30)
        elem.send_keys(args.password)

        logger.debug("clicking the login button")
        elem = get_elem(driver, "xpath", "/html/body/div[2]/div[2]/div/form/input[5]", 30)
        elem.click()

        logger.info("logged in...")

        logger.info("opening {}'s page...".format(args.host))

        driver.get("https://chaturbate.com/{}/".format(args.host))

        '''
        elem = get_elem(driver, "xpath", "/html/body/div[3]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div[last()]", 30)
        while ("chat disconnected" in elem.text) or ("trying to reconnect" in elem.text):  # not sure this'll work...
            logger.debug("chat disconnected, sleeping for 1")
            time.sleep(1)
            elem = get_elem(driver, "xpath", "/html/body/div[3]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div[last()]",
                            30)
        '''

        logger.info("sleeping for 30 for the chat to init")
        time.sleep(30)

        logger.info("ready to work...")

        if args.interval_modulo != 0:
            while int_time() % args.interval_modulo != 0:
                time.sleep(1)

        while total_tokens < args.token_limit:
            if int_time() % args.interval != 0:
                time.sleep(1)
                continue

            logger.info("executing tip")

            logger.debug("clicking the tip_button")
            elem = get_elem(driver, "class", "tip_button", 30)
            elem.click()

            logger.debug("filling the tip amount")
            elem = get_elem(driver, "id", "id_tip_amount", 30)
            elem.clear()
            elem.send_keys(args.amount)

            logger.debug("entering the tip message")
            elem = get_elem(driver, "id", "id_tip_msg_input", 30)
            elem.clear()
            elem.send_keys(args.tip_message)

            if args.defang == True:
                logger.info("running in defang mode, not actually tipping...")
                continue

            logger.debug("click the tip submit button")
            elem = get_elem(driver, "id", "id_tip_message", 30)
            elem.click()

        logger.info("hit the tip limit, exiting")
        try_to_close_the_browser(args, logger, driver)
    except KeyboardInterrupt:
        logger.info("shutting down at {}".format(int_time()))
        try_to_close_the_browser(args, logger, driver)
        pass
    except BaseException as ex:
        logger.error("something bad happened: {}".format(ex))
        try_to_close_the_browser(args, logger, driver)