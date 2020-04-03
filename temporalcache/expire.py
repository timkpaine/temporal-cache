import datetime
import pytz
import time
from functools import wraps, lru_cache
from frozendict import frozendict
from tzlocal import get_localzone
from .persistent_lru_cache import persistent_lru_cache
from .utils import should_expire, TCException


def expire(second=None, minute=None, hour=None, day=None, day_of_week=None, week=None, month=None, tz=None, maxsize=128, persistent='', custom=None, **kwargs):
    '''Expires all entries in the cache @ whole number time

        for example, @expire(0, 30, 16) will expire the cache at 4:30pm every day
    '''
    if not any((second is not None, minute is not None, hour is not None, day is not None, week is not None, month is not None)):
        second = 0

    if second is not None and second >= 60:
        raise TCException('second must be < 60')

    if minute is not None and minute >= 60:
        raise TCException('minute must be < 60')

    if hour is not None and hour >= 24:
        raise TCException('minute must be < 24')

    if day is not None and (day <= 0 or day > 31):
        raise TCException('day must be > 0, < 32')
    # elif day is not None:
    #     day += 1  # for convenience

    if day_of_week is not None and (day_of_week <= 0 or day > 8):
        raise TCException('day_of_weel must be > 0, < 8')

    if week is not None and (week <= 0 or week > 5):
        raise TCException('day must be > 0, < 6')
    # elif week is not None:
    #     week += 1  # for convenience

    if month is not None and (month <= 0 or month > 12):
        raise TCException('month must be >0, < 13')
    # elif month is not None:
    #     month += 1  # for convenience

    try:
        tz = tz or get_localzone()
    except AttributeError:
        tz = time.tzname[time.daylight]

    if isinstance(tz, str):
        try:
            tz = pytz.timezone(tz)
        except pytz.UnknownTimeZoneError:
            tz = datetime.tzinfo(tz)

    def _wrapper(foo):
        last = datetime.datetime.now(tz=tz)

        if custom:
            foo = custom(**kwargs)(foo)
        elif persistent:
            foo = persistent_lru_cache(persistent, maxsize=maxsize)(foo)
        else:
            foo = lru_cache(maxsize)(foo)

        @wraps(foo)
        def _wrapped_foo(*args, **kwargs):
            nonlocal last

            now = datetime.datetime.now(tz=tz)
            if should_expire(last, now, second, minute, hour, day, day_of_week, week, month):
                foo.cache_clear()
            last = now

            args = tuple([frozendict(arg) if isinstance(arg, dict) else tuple(arg) if isinstance(arg, list) else arg for arg in args])
            kwargs = {k: frozendict(v) if isinstance(v, dict) else tuple(v) if isinstance(v, list) else v for k, v in kwargs.items()}

            return foo(*args, **kwargs)
        return _wrapped_foo
    return _wrapper


def minutely(on=0, tz=None, maxsize=128, persistent='', custom=None, **kwargs):
    def _wrapper(foo):
        return expire(second=on, tz=tz, maxsize=maxsize, persistent=persistent, custom=custom, **kwargs)(foo)
    return _wrapper


def hourly(on=0, tz=None, maxsize=128, persistent='', custom=None, **kwargs):
    def _wrapper(foo):
        return expire(minute=on, tz=tz, maxsize=maxsize, persistent=persistent, custom=custom, **kwargs)(foo)
    return _wrapper


def daily(on=0, tz=None, maxsize=128, persistent='', custom=None, **kwargs):
    def _wrapper(foo):
        return expire(hour=on, tz=tz, maxsize=maxsize, persistent=persistent, custom=custom, **kwargs)(foo)
    return _wrapper


def monthly(on=0, tz=None, maxsize=128, persistent='', custom=None, **kwargs):
    def _wrapper(foo):
        return expire(day=on, tz=tz, maxsize=maxsize, persistent=persistent, custom=custom, **kwargs)(foo)
    return _wrapper
