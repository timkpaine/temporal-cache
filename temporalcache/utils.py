from functools import lru_cache
from six import with_metaclass
from abc import ABCMeta, abstractmethod


class TCException(Exception):
    pass


class StorageBase(with_metaclass(ABCMeta)):
    @abstractmethod
    def cache_clear(self):
        pass


def _base(last, now, lap, offset, multiple, attr):
    '''
    last - last datetime
    now - current datetime
    lap - at what point to "roll over"
    offset - how many seconds between laps
    attr - what to look at
    multiple - what to multiply attr by to get seconds
    '''
    # last started before :X, so if now > :X
    diff = round(now.timestamp(), 0) - round(last.timestamp(), 0)
    min_gap = offset - getattr(last, attr) * multiple
    if diff > offset:
        return True
    if getattr(last, attr) < lap:
        if getattr(now, attr) >= lap:
            return True
        return False
    # last started after :X, so if now > last + interval, or if now > :X
    elif getattr(now, attr) >= lap and diff >= min_gap:
        return True
    return False


def _secondly(last, now, secondly):
    return _base(last, now, secondly, 60, 1, 'second')


def _minutely(last, now, minutely):
    return _base(last, now, minutely, 3600, 60, 'minute')


def _hourly(last, now, hourly):
    return _base(last, now, hourly, 3600 * 24, 3600, 'hour')


def _daily(last, now, daily):
    return _base(last, now, daily, 3600 * 24 * 30, 3600 * 24, 'day')  # FIXME day should be derived from calendar


def _day_of_week(last, now, day_of_week):
    return _base(last, now, day_of_week, 3600 * 24 * 7, 3600 * 24, 'day')


def _weekly(last, now, weekly):
    return _base(last, now, weekly, 3600 * 24 * 7 * 4.34, 3600 * 24 * 7, 'week')  # FIXME # of weeks should be derived from calendar


def _monthly(last, now, monthly):
    return _base(last, now, monthly, 3600 * 24 * 365, 3600 * 24 * 7 * 4.34, 'month')  # FIXME # of weeks should be derived from calendar


def should_expire(last, now, secondly=None, minutely=None, hourly=None, daily=None, day_of_week=None, weekly=None, monthly=None, maxsize=128):
    '''should the cache expire?
    last - datetime
    now - datetime

    if yearly:
        necessary_distance = calc(0, 0, 0, 0, 0, 0, yearly)
    '''
    sec_res = _secondly(last, now, secondly) if secondly is not None else True
    min_res = _minutely(last, now, minutely) if minutely is not None else True
    hou_res = _hourly(last, now, hourly) if hourly is not None else True
    dow_res = _day_of_week(last, now, day_of_week) if day_of_week is not None else True
    dai_res = _daily(last, now, daily) if daily is not None else True
    wee_res = _weekly(last, now, weekly) if weekly is not None else True
    mon_res = _monthly(last, now, monthly) if weekly is not None else True
    return all((sec_res, min_res, hou_res, dai_res, dow_res, wee_res, mon_res))


@lru_cache(1000)
def calc(seconds=0, minutes=0, hours=0, days=0, weeks=0, months=0, years=0):
    return seconds + \
        minutes * 60 + \
        hours * 60 * 60 + \
        days * 24 * 60 * 60 + \
        weeks * 7 * 24 * 60 * 60 + \
        months * 30 * 7 * 24 * 60 * 60 + \
        years * 365 * 24 * 60 * 60
