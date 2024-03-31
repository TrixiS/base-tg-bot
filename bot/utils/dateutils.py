import datetime

import pytz

MSK_TIMEZONE = pytz.timezone("Europe/Moscow")


def utc_now():
    return datetime.datetime.now(pytz.UTC)


def msk_now():
    return datetime.datetime.now(MSK_TIMEZONE)
