# settings.py
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path="./")

APP_SETTINGS = {
    "APP_NAME": "kniebeugen-folter",
    "LOG_FILE": "logs/kniebeugen-folter.json.log",
    "LOG_LEVEL": logging.getLevelName(logging.DEBUG),
}

for k, v in APP_SETTINGS.items():
    c_v = os.getenv("OV_{}".format(k))
    if (bool(c_v and c_v.strip())):
        value = os.getenv("OV_{}".format(k))
        if (APP_SETTINGS[k] == True or APP_SETTINGS[k] == False):
            if (value == 1):
                value = True
            else:
                value = False
        APP_SETTINGS[k] = value