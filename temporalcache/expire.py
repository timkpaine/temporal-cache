import datetime
from functools import wraps, lru_cache
from .utils import should_expire, TCException


def expire(second=None, minute=None, hour=None, day=None, week=None, month=None, maxsize=128):
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
    elif day is not None:
        day += 1  # for convenience

    if week is not None and (week <= 0 or week > 5):
        raise TCException('day must be > 0, < 6')
    elif week is not None:
        week += 1  # for convenience

    if month is not None and (month <= 0 or month > 12):
        raise TCException('month must be < 5')
    elif month is not None:
        month += 1  # for convenience

    def _wrapper(foo):
        last = datetime.datetime.now()

        foo = lru_cache(maxsize)(foo)

        @wraps(foo)
        def _wrapped_foo(*args, **kwargs):
            nonlocal last

            now = datetime.datetime.now()
            if should_expire(last, now, second, minute, hour, day, week, month):
                foo.cache_clear()

            last = now
            return foo(*args, **kwargs)
        return _wrapped_foo
    return _wrapper
